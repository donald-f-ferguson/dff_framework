import pymysql
from .BaseDataService import BaseDataService


class MySQLRDBDataService(BaseDataService):
    """
    A generic data service for MySQL databases. The class implements common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)
        if context is None:
            self.context = dict()

    def _get_connection(self, autocommit: bool = True):
        """
        Open a connection to a database. The connection information is in the context injected
        when the object was created. If there is no information, the connection in format is common
        default values.

        :param autocommit: If True, set autocommit to be true for the connection.
        :return: A connection with DictCursor for the cursor and query.
        """
        connection = pymysql.connect(
            host=self.context.get("host", "localhost"),
            port=self.context.get("port", 3306),
            user=self.context.get("user", "root"),
            password=self.context.get("password", "dbuserdbuser"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=autocommit
        )
        return connection

    def _get_cursor(self, connection: pymysql.Connection = None, autocommit: bool = True):
        """
        Create and return a cursor.

        :param connection: The connection to use to create the cursor. The method creates one
            if it does not receive one.
        :param autocommit: If creating a connection, what is the request autocommit model.
        :return: PyMYSQL DictCursor.
        """
        if connection is None:
            connection = self._get_connection(autocommit=autocommit)
        result = connection.cursor()
        return result

    def run_query(self,
                  query: str,
                  params: list = None,
                  return_results=True,
                  connection=None,
                  cursor=None,
                  commit=True):
        """
        A helper/generic method for running a query.

        :param query: An SQL query that may contain slots for parameters, e.g. %s
        :param params: Values for the parameters.
        :param return_results: If True, fetchall() and return the data result. Otherwise, just
            return "rows affected."
        :param connection: The connection to use. The method creates one if it does not receive one.
        :param cursor: The cursor to use. The method creates one if it does not receive one.
        :param commit: Commit after executing the query.
        :return: Either the result dataset or number of rows affected.
        """


        connection_created = False
        cursor_created = False
        result = None

        if connection is None:
            # Create a connection with the proper commit mode.
            connection = self._get_connection(commit)
            connection_created = True

        if cursor is None:
            cursor = self._get_cursor(connection=connection, autocommit=commit)
            cursor_created = True

        try:
            full_query = cursor.mogrify(query, params)
            print("run_query: full_query = ", full_query, "\n")
            res = cursor.execute(query, params)

            if return_results:
                result = cursor.fetchall()
            else:
                result = res

            if commit:
                connection.commit()

        except pymysql.Error as pe:
            if commit:
                connection.rollback()
            print("run_query exception: ", pe)

        if cursor_created:
            cursor.close()
        if connection_created:
            connection.close()

        return result

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        # TODO -- Update to use run_query()

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                            f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result
