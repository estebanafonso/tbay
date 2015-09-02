from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, backref


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    seller_id = Column(Integer, ForeignKey('user.id'))
    bids = relationship("Bid", backref="bidItem")
    
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items_selling = relationship("Item", backref="seller")
    bids = relationship("Bid", backref="bidHolder")
    
    
class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    bidder_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    
    
Base.metadata.drop_all(engine)    
Base.metadata.create_all(engine)

ball = Item(name="ball")
bat = Item(name="bat")

bill = User(username="Bill",password="asf",items_selling=[ball])
frank = User(username="Frank", password="sdf")
susan = User(username="Susan", password="kjh")

bill.items_selling.append(bat)

bidFrankBat = Bid(price=4,bidHolder=frank,bidItem=bat)
bidSusanBat = Bid(price=3,bidHolder=susan,bidItem=bat)

session.add_all([bill,ball,bat,frank,susan,bidFrankBat,bidSusanBat])
session.commit()

#for item in bill.items_selling:
#    print item.name
#print bat.seller_id.username

for item in bill.items_selling:
    print item.name
print bat.seller.username

for bid in bat.bids:
    print bid.bidHolder.username
    print bid.price