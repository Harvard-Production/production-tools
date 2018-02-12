import sys, os

from MySQLdb import Error as Error

from ReaderBase import ReaderBase

class DatasetReader(ReaderBase):
    '''Class to read project tables

    This class can read and compute with project information

    Arguments:
        object {[type]} -- [description]
    '''

    def __init__(self):
        super(DatasetReader, self).__init__()
        pass


    def file_ids(self, dataset, filenames):
        '''Return a list of primary keys for the datasets specified

        Arguments:
            parents {[type]} -- [description]
        '''
        table_name = "{0}_metadata".format(dataset)
        id_query_sql = '''
            SELECT id
            FROM {table}
            WHERE filename=?
        '''.format(table=table_name)

        with self.connect() as conn:
            try:
                conn.execute(id_query_sql, filenames)
            except Error as e:
                print e
                return None

            return conn.fetchall()

    def file_query(self, **kwargs):
        where = []
        feed_list = []

        if not kwargs:
            return None, None

        for key, value in kwargs.iteritems():
            where.append(str(key) + " = %s")
            feed_list.append(value)

        return where, feed_list

    def count_files(self, dataset, **kwargs):

        table_name = "{0}_metadata".format(dataset)

        where, feed_list = self.file_query(**kwargs)

        if where is not None:
            wherestring = ' AND '.join(where)
            count_sql = '''
                SELECT COUNT(id)
                FROM {table}
                WHERE {where}
            '''.format(table=table_name, where=wherestring)

        else:
            count_sql = '''
                SELECT COUNT(id)
                FROM {table}
            '''.format(table=table_name)

        with self.connect() as conn:

            if feed_list is not None:
                conn.execute(count_sql, feed_list)
            else:
                conn.execute(count_sql)
            results = conn.fetchone()[0]

        return results


    def sum(self, dataset, target, **kwargs):

        table_name = "{0}_metadata".format(dataset)

        where, feed_list = self.file_query(**kwargs)

        if where is not None:
            wherestring = ' AND '.join(where)
            count_sql = '''
                SELECT SUM({target})
                FROM {table}
                WHERE {where}
            '''.format(target=target, table=table_name, where=wherestring)

        else:
            count_sql = '''
                SELECT SUM({target})
                FROM {table}
            '''.format(target=target, table=table_name)

        with self.connect() as conn:

            if feed_list is not None:
                conn.execute(count_sql, feed_list)
            else:
                conn.execute(count_sql)
            results = conn.fetchone()[0]

        return results

    def list_file_locations(self, dataset):

        table_name = "{0}_metadata".format(dataset)
        file_location_sql = '''
            SELECT location from {table}
        '''.format(table=table_name)

        with self.connect() as conn:
            conn.execute(file_location_sql)
            return conn.fetchall()