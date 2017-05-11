-- Prepended SQL commands --
DO
$body$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_extension
      WHERE  extname = 'uuid-ossp') THEN
         CREATE EXTENSION "uuid-ossp"
         WITH SCHEMA public;
   END IF;
END
$body$;

DO
$body$
BEGIN
   IF NOT EXISTS (
      SELECT *
      FROM   pg_catalog.pg_extension
      WHERE  extname = 'postgis') THEN
         CREATE EXTENSION "postgis"
         WITH SCHEMA public;
   END IF;
END
$body$;
---

-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.0-beta
-- PostgreSQL version: 9.6
-- Project Site: pgmodeler.com.br
-- Model Author: Dr. Horst Düster / Sourcepole

SET check_function_bodies = false;
-- ddl-end --

-- -- object: hdus | type: ROLE --
-- -- DROP ROLE IF EXISTS hdus;
-- CREATE ROLE hdus WITH 
-- 	SUPERUSER
-- 	CREATEDB
-- 	CREATEROLE
-- 	INHERIT
-- 	LOGIN
-- 	REPLICATION
-- 	ENCRYPTED PASSWORD '********';
-- -- ddl-end --
-- 
-- -- object: hdus_cp | type: ROLE --
-- -- DROP ROLE IF EXISTS hdus_cp;
-- CREATE ROLE hdus_cp WITH 
-- 	SUPERUSER
-- 	INHERIT
-- 	ENCRYPTED PASSWORD '********'
-- 	VALID UNTIL '2129-03-25 00:00';
-- -- ddl-end --
-- 

-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: historisierung | type: DATABASE --
-- -- DROP DATABASE IF EXISTS historisierung;
-- CREATE DATABASE historisierung
-- 	ENCODING = 'UTF8'
-- 	LC_COLLATE = 'de_DE.UTF-8'
-- 	LC_CTYPE = 'de_DE.UTF-8'
-- 	TABLESPACE = pg_default
-- ;
-- -- ddl-end --
-- 

-- object: hist_tabs | type: SCHEMA --
-- DROP SCHEMA IF EXISTS hist_tabs CASCADE;
CREATE SCHEMA hist_tabs;
-- ddl-end --

SET search_path TO pg_catalog,public,hist_tabs;
-- ddl-end --

-- object: hist_tabs.historic_record | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs.historic_record() CASCADE;
CREATE FUNCTION hist_tabs.historic_record ()
	RETURNS trigger
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
  DECLARE 
    pkey_rec record;
    pkey_string TEXT;
    
  BEGIN	

-- Get primarykey columns of relation
     pkey_string := '';
 
     FOR pkey_rec IN select col.column_name 
                     from information_schema.table_constraints as key,
                          information_schema.key_column_usage as col
                     where key.table_schema = TG_TABLE_SCHEMA::name
                       and key.table_name = TG_TABLE_NAME::name
                       and key.constraint_type='PRIMARY KEY'
                       and key.table_catalog = col.table_catalog
                       and key.table_schema = col.table_schema
                       and key.table_name = col.table_name
      LOOP

        pkey_string := pkey_string||' and '||pkey_rec.column_name||' = $1.'||pkey_rec.column_name;
      END LOOP;

      pkey_string := ltrim(pkey_string,' and ');
      
     if TG_OP = 'INSERT' THEN
        execute 'insert into '||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' select $1.*, nextval(''' ||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||'_hist_id_seq''), now(), NULL, current_user' USING NEW;
        RETURN NEW;
     ELSEIF TG_OP = 'UPDATE' THEN
        execute format('update ' ||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' 
                 set valid_to = now() 
                 where hist_id in (
                   select max(hist_id) 
                   from hist_tabs.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' 
                   where %1$s);',  pkey_string) USING OLD;
        execute 'insert into '||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' select $1.*, nextval(''' ||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||'_hist_id_seq''), now(), NULL, current_user' USING NEW;
         RETURN OLD;
     ELSEIF TG_OP = 'DELETE' THEN
        execute format('update ' ||quote_ident('hist_tabs') ||'.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' 
                 set valid_to = now() 
                 where hist_id in (
                   select max(hist_id) 
                   from hist_tabs.'|| quote_ident(TG_TABLE_SCHEMA ||'_'|| TG_TABLE_NAME) ||' 
                   where %1$s);',  pkey_string) USING OLD;

         RETURN OLD;
     END IF;                         
 END;
$$;
-- ddl-end --

-- object: hist_tabs.update | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs.update(character varying,character varying,boolean,character varying) CASCADE;
CREATE FUNCTION hist_tabs.update ( _param1 character varying,  _param2 character varying,  _param4 boolean DEFAULT true,  _param3 character varying DEFAULT ' ')
	RETURNS boolean
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
DECLARE
  in_new_layer ALIAS FOR $1;
  in_old_layer ALIAS FOR $2;
  has_geometry ALIAS FOR $3;
  in_exclude_string ALIAS FOR $4;
  exclude_string TEXT;
  old_exclude_fields TEXT;
  new_exclude_fields TEXT;  
  result record;
  new_layer TEXT;
  old_layer TEXT;
  old_schema TEXT;
  new_schema TEXT;
  old_pkey_rec RECORD;
  new_pkey_rec RECORD;
  old_pkey TEXT;
  new_pkey TEXT;		
  att_check RECORD;
  attributes RECORD;
  qry_update TEXT;
  qry_insert TEXT;	
  field_list TEXT;
  old_fields TEXT;
  n_arch_field TEXT;
  arch_fields TEXT;
  where_fields TEXT;
  old_geo_rec RECORD;
  old_geom_col TEXT;
  new_geo_rec RECORD;
  new_geom_col TEXT;
  pos INTEGER;
  integer_var INTEGER;		
  insub_query TEXT;
  qry TEXT;
  old_pkey_string TEXT;
  new_pkey_string TEXT;
  testRec RECORD;
  
  
  BEGIN
    pos := strpos(in_old_layer,'.');
    if pos=0 then 
        old_schema := 'public';
  	old_layer := in_old_layer; 
    else 
  	old_schema = substr(in_old_layer,0,pos);
  	pos := pos + 1; 
        old_layer = substr(in_old_layer,pos);
    END IF;
  
    pos := strpos(in_new_layer,'.');
    if pos=0 then 
        new_schema := 'public';
  	new_layer := in_new_layer; 
    else 
        new_schema = substr(in_new_layer,0,pos);
  	pos := pos+1; 
  	new_layer = substr(in_new_layer,pos);
    END IF;
  
    select into testRec table_name
    from information_schema.tables
    where table_schema = old_schema::name
      and table_name = old_layer::name;
   
    IF NOT FOUND THEN
       RAISE EXCEPTION 'Table %.% does not exist', old_schema,old_layer;
    END IF; 

    select into testRec table_name
    from information_schema.tables
    where table_schema = new_schema::name
      and table_name = new_layer::name;
   
    IF NOT FOUND THEN
       RAISE EXCEPTION 'Table %.% does not exist', new_schema,new_layer;
    END IF; 

  
  -- Vorbelegen der Variablen
    old_pkey_string := '';
    new_pkey_string := '';
    field_list := '';
    old_fields := '';		
    qry_insert := '';
    qry_update := '';
    integer_var := 0;
  
  		
  -- exlude-string formulieren
     qry := format('SELECT COUNT(*) FROM regexp_matches(''%1$s'', '','', ''g'')', in_exclude_string);
     execute qry into result;
     integer_var := result.count+1;
     exclude_string := '''''';
     for r in 1 .. integer_var
     LOOP
       qry := format('select split_part(''%1$s'', '','', %2$s)', in_exclude_string, r);
       execute qry into result;
       exclude_string := exclude_string||','''||result.split_part||'''';
     END LOOP;
     IF has_geometry THEN  
  -- Feststellen wie die Geometriespalte der Layer heisst bzw. ob der Layer in der Tabelle geometry_columns definiert ist
       select into old_geo_rec f_geometry_column, type as geom_type 
       from public.geometry_columns 
       where f_table_schema = old_schema 
         and f_table_name = old_layer;

       IF NOT FOUND THEN
         RAISE EXCEPTION 'Table %.% has no geometry. Please call update with geometry=False', old_schema, old_layer;
       END IF;
 
       old_geom_col := old_geo_rec.f_geometry_column;
  	  
       select into new_geo_rec f_geometry_column, type as geom_type 
       from public.geometry_columns 
       where f_table_schema = new_schema 
        and  f_table_name = new_layer;

       IF NOT FOUND THEN
         RAISE EXCEPTION 'Table %.% has no geometry. Please call update with geometry=False', new_schema, new_layer;
       END IF;

  
       new_geom_col := new_geo_rec.f_geometry_column;
       old_exclude_fields := ''''||old_geom_col||''','||exclude_string;
       new_exclude_fields := ''''||new_geom_col||''','||exclude_string;
     ELSE
       old_exclude_fields := exclude_string;
       new_exclude_fields := exclude_string;     
     END IF;
     
     
     
  -- Pruefen, ob der new_layer mindestens der Struktur des old_layer entspricht	
     qry := format('select col.column_name
     from information_schema.columns as col
     where table_schema = ''%1$s''
       and table_name = ''%2$s''
       and (position(''nextval'' in lower(column_default)) is NULL or position(''nextval'' in lower(column_default)) = 0)		
       and col.column_name not in (%3$s)
     except
     select col.column_name
     from information_schema.columns as col
     where table_schema = ''%4$s''
       and table_name = ''%5$s''
       and col.column_name not in (%6$s);', old_schema, old_layer, old_exclude_fields, new_schema, new_layer, new_exclude_fields);
       
     execute qry into att_check;
    GET DIAGNOSTICS integer_var = ROW_COUNT;
    	
    IF integer_var > 0 THEN
       RAISE EXCEPTION 'Die Tabelle % entspricht nicht der Tabelle %', new_layer, old_layer;
       RETURN False;
    END IF;
    IF has_geometry THEN
      qry := format('select st_geometrytype(%3$s.%4$s.%1$s) as old_type, st_geometrytype(%5$s.%6$s.%2$s) as new_type from %3$s.%4$s, %5$s.%6$s 
                     where st_geometrytype(%3$s.%4$s.%1$s) <> st_geometrytype(%5$s.%6$s.%2$s)', 
                     old_geom_col, new_geom_col, old_schema, old_layer, new_schema, new_layer);
      execute qry into att_check;
      GET DIAGNOSTICS integer_var = ROW_COUNT;
    	
      IF integer_var > 0 THEN
         RAISE EXCEPTION 'Die Tabellen haben unterschiedliche Geometrietypen % vs %', att_check.old_type, att_check.new_type;
         RETURN False;
      END IF;
    END IF;
   
    n_arch_field := ' ';
    arch_fields:=' ';
    where_fields:=' ';
  		
  		
  -- Pruefen ob und welche Spalte der Primarykey der Tabelle old_layer ist 
--    EXECUTE format('select * from hist_tabs._primarykey(''%1$s.%2$s'')', old_schema, old_layer) INTO old_pkey_rec;    

    for old_pkey_rec IN EXECUTE format('select * from hist_tabs._primarykey(''%1$s.%2$s'')', old_schema, old_layer) LOOP
	old_pkey_string = old_pkey_string||'||o."'||old_pkey_rec.pkey_column||'"';
	RAISE NOTICE '%', old_pkey_rec.pkey_column;
    END LOOP;
    
    old_pkey_string := ltrim(old_pkey_string, '||');
  
  -- Prfen ob und welche Spalte der Primarykey der Tabelle new_layer ist
    for new_pkey_rec IN EXECUTE format('select * from hist_tabs._primarykey(''%1$s.%2$s'')', new_schema, new_layer) LOOP
	new_pkey_string = new_pkey_string||'||n."'||new_pkey_rec.pkey_column||'"';
    END LOOP;
    
    new_pkey_string := ltrim(new_pkey_string, '||');
  				
    IF has_geometry THEN    
      insub_query := format('select %1$s as id 
  	                from "%2$s"."%3$s" as o
    	                except 
   			        select %1$s 
  			        from "%4$s"."%5$s" as n,"%2$s"."%3$s" as o 
  			        where md5(o."%6$s"::TEXT)=md5(n."%7$s"::TEXT) 
  			          and o."%6$s" && n."%7$s"', 
                    old_pkey_string, old_schema, old_layer, new_schema, new_layer, 
                    old_geo_rec.f_geometry_column, new_geo_rec.f_geometry_column);	
    ELSE
      insub_query := format('select %1$s as id 
  	                from "%2$s"."%3$s" as o
    	                except 
   			        select %1$s 
  			        from "%4$s"."%5$s" as n,"%2$s"."%3$s" as o 
  			        where 1 = 1 ', 
                    old_pkey_string, old_schema, old_layer, new_schema, new_layer);
    END IF;

      		
  -- Alle Sequenzen ermitteln und unbercksichtigt lassen		
    qry := format('select column_name as att, data_type as typ
                   from information_schema.columns as col
                   where table_schema = ''%1$s''
                   	and table_name = ''%2$s''
                   	and column_name not in (%3$s)
                        and (position(''nextval'' in lower(column_default)) is NULL 
                        or position(''nextval'' in lower(column_default)) = 0)',
                   old_schema, old_layer, old_exclude_fields);
  -- Alle Sequenzen ermitteln und unbercksichtigt lassen		
    FOR attributes IN EXECUTE qry 			
    LOOP
    old_fields := old_fields ||format(',"%1$s"::%2$s', attributes.att, attributes.typ);
    field_list := field_list ||format(',"%1$s"', attributes.att);
    
  -- Eine Spalte vom Typ Bool darf nicht in die Coalesce-Funktion gesetzt werden					 
--    IF old_pkey_rec.pkey_column <> attributes.att THEN
       IF attributes.typ = 'bool' THEN
           where_fields := where_fields ||format(' and n."%1$s"=o."%1$s"', attributes.att);					 
       ELSE
  	   where_fields := where_fields ||format(' and coalesce(n."%1$s"::text,'''')=coalesce(o."%1$s"::text,'''')', attributes.att);
       END IF;
--     END IF;
  
    END LOOP;
  		
    where_fields := where_fields||' '||arch_fields;
    insub_query := insub_query||' '||where_fields;
  
  -- Vorbereiten der Update Funktion
    qry_update := 'delete from "'||old_schema||'"."'||old_layer||'" as o
    where '||old_pkey_string||'
      in ('||insub_query||');';
  									   
  -- Ausfuehren der Update Funktion 
  EXECUTE qry_update;
  GET DIAGNOSTICS integer_var = ROW_COUNT;
  RAISE NOTICE ' % Objekte wurden im Layer %.% archiviert',integer_var,old_schema,old_layer;
  

  -- Vorbereiten der Insert Funktion
  IF has_geometry THEN
    insub_query := format('select "%1$s" as "%2$s"'||old_fields||' 
                    from %4$s.%5$s as n
  		          where %3$s in (
  		            select %3$s as id from "%4$s"."%5$s" as n
  		            except
  		            select %3$s 
  		            from "%4$s"."%5$s" as n,"%6$s"."%7$s" as o 
  		            where md5(n."%1$s"::TEXT)=md5(o."%2$s"::TEXT) 
  		            and o."%2$s" && n."%1$s" '||where_fields||' )'||n_arch_field||'',
                   new_geo_rec.f_geometry_column, old_geo_rec.f_geometry_column, new_pkey_string, new_schema, new_layer, old_schema, old_layer);
  														
    qry_insert := 'insert into "'||old_schema||'"."'||old_layer||'" ("'||old_geo_rec.f_geometry_column||'"'||field_list||') '||insub_query;
  ELSE
    insub_query := format('select '||ltrim(old_fields,',')||' 
                    from %2$s.%3$s as n
  		          where %1$s in (
  		            select %1$s as id from "%2$s"."%3$s" as n
  		            except
  		            select %1$s 
  		            from "%2$s"."%3$s" as n,"%4$s"."%5$s" as o 
  		            where '||ltrim(where_fields,' and')||' )'||n_arch_field||'',
                   new_pkey_string, new_schema, new_layer, old_schema, old_layer);
  														
    qry_insert := 'insert into "'||old_schema||'"."'||old_layer||'" ('||ltrim(field_list,',')||') '||insub_query;
    
  END IF;  
  EXECUTE qry_insert;
  GET DIAGNOSTICS integer_var = ROW_COUNT;
  RAISE NOTICE ' % Objekte wurden in den Layer %.% neu eingefuegt',integer_var,old_schema,old_layer;
  
  RETURN true;
END;
$$;
-- ddl-end --

-- object: hist_tabs.init | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs.init(IN character varying,IN boolean) CASCADE;
CREATE FUNCTION hist_tabs.init (IN _param1 character varying, IN _param2 boolean DEFAULT False)
	RETURNS boolean
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
DECLARE
    inTable ALIAS FOR $1;
    recursiv ALIAS FOR $2;
    table_rec record;

  BEGIN	
    IF recursiv THEN
      for table_rec in 
        select table_name
        from information_schema.tables
        where table_type = 'BASE TABLE'
          and table_schema = inTable::name
      LOOP
        EXECUTE format('select hist_tabs._table_init(''%1$s.%2$s'')', inTable, table_rec.table_name);
      END LOOP;
    ELSE
      EXECUTE format('select hist_tabs._table_init(''%1$s'')', inTable);
    END IF;
          
                
    RETURN true ;
  END;
$$;
-- ddl-end --

-- object: hist_tabs.version | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs.version(anyelement,date) CASCADE;
CREATE FUNCTION hist_tabs.version ( _tbl_type anyelement,  _date date)
	RETURNS SETOF anyelement
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	ROWS 1000
	AS $$
DECLARE
  qry TEXT;
  h_tab TEXT;
  pos INTEGER;
  my_schema TEXT;
  my_table TEXT;
  pkey_rec record;
  pkey_string TEXT;
  testRec RECORD;
  
BEGIN
   pos := strpos(pg_typeof(_tbl_type)::TEXT,'.');
   if pos = 0 then 
        my_schema := 'public';
        my_table := pg_typeof(_tbl_type)::TEXT;
        h_tab := 'hist_tabs.'||quote_ident('public_'||pg_typeof(_tbl_type)::TEXT);        
   else 
        my_schema := substr(pg_typeof(_tbl_type)::TEXT,0,pos);
        pos := pos + 1; 
        my_table := substr(pg_typeof(_tbl_type)::TEXT,pos);
        h_tab := 'hist_tabs.'||quote_ident(my_schema||'_'||my_table);
   END IF;  
   

    select into testRec table_name
    from information_schema.tables
    where table_schema = my_schema::name
      and table_name = my_table::name;
   
    IF NOT FOUND THEN
       RAISE EXCEPTION 'Table %.% does not exist', my_schema,my_table;
    END IF; 

   pkey_string := '';

   
   for pkey_rec IN EXECUTE format('select * from hist_tabs._primarykey(''%1$s.%2$s'')', my_schema, my_table) LOOP
	pkey_string := pkey_string||','||pkey_rec.pkey_column;
   END LOOP;
    
   pkey_string := ltrim(pkey_string, ',');   
   
   qry := (SELECT format('
      with timecut as (SELECT max(hist_id) as hist_id
      FROM   %3$s   
      WHERE  valid_from::date < ''%4$s''::date AND ( valid_to::date >= ''%4$s''::date OR valid_to IS NULL ) 
      GROUP BY %5$s, valid_from::date)

      SELECT %1$s 
      FROM timecut, %3$s
      WHERE timecut.hist_id = %3$s.hist_id '
    , string_agg(quote_ident(attname), ', '), pg_typeof(_tbl_type)::TEXT, h_tab, _date, pkey_string )

     FROM   pg_attribute
     WHERE  attrelid = pg_typeof(_tbl_type)::text::regclass
       AND NOT attisdropped  -- no dropped (dead) columns
       AND attnum > 0        -- no system columns      
       AND attname not in ('hist_id', 'valid_from', 'valid_to', 'dbuser') -- no historic system columns
   );
   
   RETURN QUERY EXECUTE qry;
END;

$$;
-- ddl-end --

-- object: hist_tabs._revision | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs._revision() CASCADE;
CREATE FUNCTION hist_tabs._revision ()
	RETURNS character varying
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 1
	AS $$
BEGIN
  RETURN '1.1.2';
END;
$$;
-- ddl-end --

-- -- object: hist_tabs.undo | type: FUNCTION --
-- -- DROP FUNCTION IF EXISTS hist_tabs.undo(character varying) CASCADE;
-- CREATE FUNCTION hist_tabs.undo ( tbl character varying)
-- 	RETURNS boolean
-- 	LANGUAGE plpgsql
-- 	VOLATILE 
-- 	CALLED ON NULL INPUT
-- 	SECURITY INVOKER
-- 	COST 100
-- 	AS $$
-- DECLARE
--   tbl ALIAS FOR $1;
--   qry TEXT;
--   h_tab TEXT;
--   pos INTEGER;
--   myschema TEXT;
--   mytable TEXT;
--   pkey_rec record;
--   
-- BEGIN
--     pos := 0;
--     if strpos(tbl,'.') = 0 then 
--         h_tab := 'hist_tabs.'||quote_ident('public_'||tbl);
--         myschema := 'public';
--         mytable := tbl;
--     else 
--         pos := pos + 1; 
--         h_tab := 'hist_tabs.'||quote_ident(substr(tbl,0,pos)||'_'||substr(tbl,pos));
--         myschema := quote_ident(substr(tbl,0,pos));
--         mytable := quote_ident(substr(tbl,pos));
--     END IF;  
-- 
--   -- Pruefen ob und welche Spalte der Primarykey der Tabelle
--     select into pkey_rec col.column_name 
--     from information_schema.table_constraints as key,
--          information_schema.key_column_usage as col
--     where key.table_schema = myschema::name
--       and key.table_name = mytable::name
--       and key.constraint_type='PRIMARY KEY'
--       and key.table_catalog = col.table_catalog
--       and key.table_schema = col.table_schema
--       and key.table_name = col.table_name;	
--   
--     IF NOT FOUND THEN
--         RAISE EXCEPTION 'Die Tabelle hat keinen Primarykey';
--         RETURN FALSE;
--     END IF;
-- 
-- -- Undo insert
--    qry :=  format('
--      with delete_insert as 
--       (
--         select max(valid_from) as last_insert, max(valid_to) as last_delete
--         from hist_tabs.%2$s_%3$s
--       )
--      delete from hist_tabs.%2$s_%3$s where %1$s in (
--        select %1$s 
--        from hist_tabs.%2$s_%3$s 
--        where %1$s in (
--          select %1$s 
--          from hist_tabs.%2$s_%3$s 
--          where valid_from in (
--            select last_insert 
--            from delete_insert)))', pkey_rec, myschema, mytable);
-- --   EXECUTE qry;
-- 
-- -- Undo delete     
--    qry :=  format('
--      with delete_insert as 
--       (
--         select max(valid_from) as last_insert, max(valid_to) as last_delete
--         from hist_tabs.%2$s_%3$s
--       )
--      update hist_tabs.%2$s_%3$s set valid_to = NULL where %1$s in (
--        select %1$s 
--        from hist_tabs.%2$s_%3$s 
--        where %1$s in (
--          select %1$s 
--          from hist_tabs.%2$s_%3$s 
--          where valid_to in (
--            select last_delete 
--            from delete_insert)))', pkey_rec, myschema, mytable);
-- 
--     EXECUTE qry;
-- /*
--   union
--   select 'deleted' as action, gid 
--    from hist_tabs.public_streets 
--    where gid in (select gid 
--                  from hist_tabs.public_streets 
--                  where valid_to in (select last_delete 
--                                       from delete_insert)
-- */
-- RETURN True;                                      
-- END;
-- $$;
-- -- ddl-end --
-- 
-- object: hist_tabs._primarykey | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs._primarykey(IN character varying) CASCADE;
CREATE FUNCTION hist_tabs._primarykey (IN intable character varying)
	RETURNS TABLE ( pkey_column text,  success boolean)
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
DECLARE
    mySchema TEXT;
    myTable TEXT;
    myPkeyRec RECORD;
    message TEXT;
    pos INT;

  BEGIN	
    pos := strpos(inTable,'.');
  
    if pos=0 then 
        mySchema := 'public';
  	    myTable := inTable; 
    else 
        mySchema := substr(inTable,0,pos);
        pos := pos + 1; 
        myTable := substr(inTable,pos);
    END IF;  

  -- Check if PKEY exists and which columns represents it 
    for myPkeyRec in select col.column_name 
    from information_schema.table_constraints as key,
         information_schema.key_column_usage as col
    where key.table_schema = mySchema::name
      and key.table_name = myTable::name
      and key.constraint_type='PRIMARY KEY'
      and key.constraint_name = col.constraint_name
      and key.table_catalog = col.table_catalog
      and key.table_schema = col.table_schema
      and key.table_name = col.table_name 
     LOOP
       pkey_column := myPkeyRec.column_name;     
       success := 'true';
       RETURN NEXT;   
    END LOOP;
  END;
$$;
-- ddl-end --

-- object: hist_tabs._table_init | type: FUNCTION --
-- DROP FUNCTION IF EXISTS hist_tabs._table_init(IN character varying) CASCADE;
CREATE FUNCTION hist_tabs._table_init (IN _table character varying)
	RETURNS boolean
	LANGUAGE plpgsql
	VOLATILE 
	CALLED ON NULL INPUT
	SECURITY INVOKER
	COST 100
	AS $$
DECLARE
    inTable ALIAS FOR $1;
    pos INTEGER;
    _has_geometry BOOLEAN;
    mySchema TEXT;
    myTable TEXT;
    histSchema TEXT;
    histTab TEXT;
    sql TEXT;
    geomCol TEXT;
    geomType TEXT;
    geomDIM INTEGER;
    geomSRID INTEGER;
    attributes record;
    testTab TEXT;
    testRec record;
    testPKey record;
    fields TEXT;
    mySequence TEXT;
    myPkey TEXT;
    myPkeyRec record;
    archiveWhere TEXT;
    
  BEGIN	
    histSchema := 'hist_tabs';
    pos := strpos(inTable,'.');
    fields := '';
    geomCol := '';
    geomDIM := 2;
    geomSRID := -1;
    geomType := '';
    mySequence := '';
    archiveWhere := '';

    if pos=0 then 
        mySchema := 'public';
  	    myTable := inTable; 
    else 
        mySchema = substr(inTable,0,pos);
        pos := pos + 1; 
        myTable = substr(inTable,pos);
    END IF;  

    histTab := histSchema||'.'||mySchema||'_'||myTable||'';

    select into testRec table_name
    from information_schema.tables
    where table_schema = mySchema::name
      and table_name = myTable::name;
   
    IF NOT FOUND THEN
       RAISE EXCEPTION 'Table %.% does not exist', mySchema,myTable;
       RETURN False;
    END IF;    
 
 
     select into testRec f_geometry_column, coord_dimension, srid, type
     from geometry_columns
     where f_table_schema = mySchema::name
       and f_table_name = myTable::name;
     IF NOT FOUND THEN
       _has_geometry := False;     
     ELSE
       _has_geometry := True;     
       geomCol := testRec.f_geometry_column;
       geomDIM := testRec.coord_dimension;
       geomSRID := testRec.srid;
       geomType := testRec.type;
     END IF;
     
    select into testPKey col.column_name 
    from information_schema.table_constraints as key,
         information_schema.key_column_usage as col
    where key.table_schema = mySchema::name
      and key.table_name = myTable::name
      and key.constraint_type='PRIMARY KEY'
      and key.constraint_name = col.constraint_name
      and key.table_catalog = col.table_catalog
      and key.table_schema = col.table_schema
      and key.table_name = col.table_name;	
  
    IF NOT FOUND THEN
      RAISE NOTICE 'Table %.% has no Primarykey', mySchema, myTable;
      RETURN False;
    END IF;			
       
    testTab := quote_ident(mySchema||'_'||myTable);
    select into testRec table_name
    from information_schema.tables
    where table_schema = 'hist_tabs'::name
      and table_name = testTab::name;
    IF FOUND THEN
       RAISE EXCEPTION 'Table hist_tabs.%_% already exists', mySchema,myTable;
    END IF;    
  
     
    for attributes in select *
                   from  information_schema.columns
                   where table_schema=mySchema::name
                     and table_name = myTable::name
    LOOP         
        fields := fields||','||quote_ident(attributes.column_name);
    END LOOP;
    fields := substring(fields,2);
     
    sql := format('create table %1$s (LIKE "%2$s"."%3$s");
             alter table %1$s add column hist_id bigserial;
             ALTER TABLE %1$s ADD CONSTRAINT %2$s_%3$s_pkey PRIMARY KEY(hist_id);
             alter table %1$s add column valid_from timestamp;
             alter table %1$s ALTER COLUMN valid_from set default now();
             alter table %1$s add column valid_to timestamp;
             alter table %1$s add column dbuser character varying;
             alter table %1$s ALTER COLUMN dbuser set default current_user;', histTab, mySchema, myTable);
    execute sql;
    sql := format('insert into %1$s (%4$s) select %4$s from "%2$s"."%3$s";', histTab, mySchema, myTable, fields);
    execute sql;
    IF _has_geometry THEN
       execute format('CREATE INDEX %2$s_%3$s_geo_idx ON %1$s USING gist (%4$s);', histTab, mySchema, myTable, geomCol);
    END IF;
    execute format('CREATE TRIGGER historic_record
               AFTER INSERT OR UPDATE OR DELETE
               ON "%1$s"."%2$s" 
               FOR EACH ROW
               EXECUTE PROCEDURE hist_tabs.historic_record();', mySchema, myTable);
          
                
    RETURN true ;
  END;
$$;
-- ddl-end --
ALTER FUNCTION hist_tabs._table_init(IN character varying) OWNER TO postgres;
-- ddl-end --

-- ddl-end --


-- -- object: hist_tabs.diff | type: FUNCTION --
-- -- DROP FUNCTION IF EXISTS hist_tabs.diff(character varying,date,date) CASCADE;
-- CREATE FUNCTION hist_tabs.diff ( in_table character varying,  a_date date,  b_date date DEFAULT now())
-- 	RETURNS boolean
-- 	LANGUAGE plpgsql
-- 	VOLATILE 
-- 	CALLED ON NULL INPUT
-- 	SECURITY INVOKER
-- 	COST 100
-- 	AS $$
-- DECLARE
--   pos INTEGER;
--   SQL text;
-- 
-- 
-- BEGIN
--     pos := strpos(in_table,'.');
--     if pos=0 then 
--       my_schema := 'public';
--   	  my_table := in_table; 
--     else 
--       my_schema = substr(in_table,0,pos);
--   	  pos := pos+1; 
--   	  my_table = substr(in_table,pos);
--     END IF;
--   
--     select into testRec table_name
--     from information_schema.tables
--     where table_schema = my_schema::name
--       and table_name = my_table::name;
--    
--     IF NOT FOUND THEN
--        RAISE EXCEPTION 'Table %.% does not exist', my_schema,my_table;
--     END IF; 
-- 
--     sql := format('with insert as (
--                      select * from hist_tabs.version(NULL::public.streets,''%2$s'')
--                      except
--                      select * from hist_tabs.version(NULL::public.streets,''%1$s'')
--                    ),
-- 
--                    delete as (
--                      select * from hist_tabs.version(NULL::public.streets,''%1$s'')
--                      except
--                      select * from hist_tabs.version(NULL::public.streets,''%2$s'')
--                    )
-- 
--                  select *, ''insert'' as action from insert
--                  union 
--                  select *, ''delete'' as action from delete', a_date, b_date
--     
-- 
-- END;
-- $$;
-- -- ddl-end --
-- ALTER FUNCTION hist_tabs.diff(character varying,date,date) OWNER TO postgres;
-- -- ddl-end --
-- 

