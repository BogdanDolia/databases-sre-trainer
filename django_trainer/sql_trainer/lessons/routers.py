class LessonsRouter:
    """
    A router to control database operations for models.
    """
    
    # All models will be stored in the default database for now
    # This ensures migrations succeed without complex relations
    
    def db_for_read(self, model, **hints):
        """All reads go to default database"""
        return 'default'

    def db_for_write(self, model, **hints):
        """All writes go to default database"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow all relations"""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow all migrations on the default database"""
        if db == 'default':
            return True
        return False