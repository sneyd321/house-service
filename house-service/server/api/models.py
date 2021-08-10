from server import db
from sqlalchemy.exc import IntegrityError, OperationalError



class House(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    homeownerId = db.Column(db.Integer())
    arrangement = db.Column(db.String(10))
    province = db.Column(db.String(30))
    isComplete = db.Column(db.Boolean())

    def __init__(self, homeownerId, **houseData):
        self.homeownerId = homeownerId
        self.arrangement = houseData.get("arrangement", "")
        self.province = houseData.get("province", "")
        self.isComplete = False
       

    def toJson(self):
        return {
            "houseId": self.id,
            "homeownerId": self.homeownerId,
            "arrangement": self.arrangement,
            "province": self.province,
            "isComplete": self.isComplete,
            "rentalUnitLocation": RentalUnitLocation.query.filter(RentalUnitLocation.houseId == self.id).first().toJson() if RentalUnitLocation.query.filter(RentalUnitLocation.houseId == self.id).first() else None
        }

 
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False


    def close_session(self):
        db.session.close()
            
    

    def update(self):
        rows = House.query.filter(House.id == self.id).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False

    def toDict(self):
        return {
            House.id : self.id,
            House.homeownerId : self.homeownerId,
        }

    def getId(self):
        return {
            "houseId": self.id
        }

   
    def __repr__(self):
        return "< House: House >"


class RentalUnitLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitName = db.Column(db.String(100))
    isCondo = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), nullable=False)
    

    def __init__(self, **rentalUnitLocationData):
        self.streetNumber = rentalUnitLocationData.get("streetNumber", "")
        self.streetName = rentalUnitLocationData.get("streetName", "")
        self.city = rentalUnitLocationData.get("city", "")
        self.province = rentalUnitLocationData.get("province", "")
        self.postalCode = rentalUnitLocationData.get("postalCode", "")
        self.unitName = rentalUnitLocationData.get("unitName", "")
        self.isCondo = rentalUnitLocationData.get("isCondo", "")
        self.houseId = rentalUnitLocationData.get("houseId", "")



    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return False
   
    def update(self):
        RentalUnitLocation.query.update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def toDict(self):
        return {
            RentalUnitLocation.streetNumber: self.streetNumber,
            RentalUnitLocation.streetName: self.streetName,
            RentalUnitLocation.city: self.city,
            RentalUnitLocation.province: self.province,
            RentalUnitLocation.postalCode: self.postalCode,
            RentalUnitLocation.unitName: self.unitName,
            RentalUnitLocation.parkingSpaces: self.parkingSpaces,
            RentalUnitLocation.isCondo: self.isCondo
        }

    def toJson(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitName": self.unitName,
            "isCondo": self.isCondo
        }

    def __repr__(self):
        return "< Rental Unit Location: " + str(self.streetNumber) + " " + self.streetName + " >"

