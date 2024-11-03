class ReadReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'replica'  # Route read queries to the replica

    def db_for_write(self, model, **hints):
        return 'default'  # Route write queries to the primary