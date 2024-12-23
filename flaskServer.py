from flask import Flask
from router import f_router
from base import ObjSql;
from sqlalchemy import Column,String,Integer
class Server():
   def __init__(self):
      self.o_app =  Flask(__name__);
   def f_router(self):
      f_router(self);
   def f_ObjSql(self):
      self.o_objSql = ObjSql();
      def f_table(Base):
         class User(Base):
            __tablename__ = "user";
            uid = Column(Integer, primary_key=True, autoincrement=True) # primary_key表示主键 autoincrement表示自增长
            name = Column(String(32));#, unique=True
            gender = Column(String(32));
         return User;	
      self.o_objSql.f_creTable(f_table);
   def f_main(self):
      self.f_router();
      self.f_ObjSql();
      self.o_app.run(debug=True);
      
o_server = Server();
o_server.f_main();
