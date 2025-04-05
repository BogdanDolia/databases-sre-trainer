"""SQL scripts for database management functions"""

# SQL to drop user-created tables (excluding Django system tables)
DROP_USER_TABLES = """
DO $$
DECLARE
    tbl_name text;
BEGIN
    FOR tbl_name IN 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        AND table_name NOT IN ('django_migrations', 'auth_group', 'auth_group_permissions', 
                            'auth_permission', 'auth_user', 'auth_user_groups', 
                            'auth_user_user_permissions', 'django_admin_log', 
                            'django_content_type', 'django_session', 
                            'lessons_lesson', 'lessons_exercise', 'lessons_userprogress')
    LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || tbl_name || ' CASCADE';
    END LOOP;
END $$;
"""

# SQL to drop all user-created views
DROP_USER_VIEWS = """
DO $$
DECLARE
    view_name text;
BEGIN
    FOR view_name IN 
        SELECT table_name 
        FROM information_schema.views 
        WHERE table_schema = 'public'
    LOOP
        EXECUTE 'DROP VIEW IF EXISTS ' || view_name || ' CASCADE';
    END LOOP;
END $$;
"""