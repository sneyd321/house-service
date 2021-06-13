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
            "homeownerLocation": HomeownerLocation.query.filter(HomeownerLocation.houseId == self.id).first().toJson() if HomeownerLocation.query.filter(HomeownerLocation.houseId == self.id).first() else None,
            "rentalUnitLocation": RentalUnitLocation.query.filter(RentalUnitLocation.houseId == self.id).first().toJson() if HomeownerLocation.query.filter(HomeownerLocation.houseId == self.id).first() else None
        }

 
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False
            
    

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


class RentDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    rentDueDate = db.Column(db.String(10))
    baseRent = db.Column(db.Integer())
    rentMadePayableTo = db.Column(db.String(200))
    parkingAmount = db.Column(db.Integer())
    parkingSpaces = db.Column(db.Integer())
    houseId = db.Column(db.Integer(), nullable=False, unique=True)
    

    def __init__(self, **rentDetailsData):
        self.rentDueDate = rentDetailsData.get("rentDueDate", "")
        self.baseRent = rentDetailsData.get("baseRent", "")
        self.rentMadePayableTo = rentDetailsData.get("rentMadePayableTo", "")
        self.parkingAmount = rentDetailsData.get("parkingAmount", "")
        self.parkingSpaces = rentDetailsData.get("parkingSpaces", "")
        self.houseId = rentDetailsData.get("houseId")

       
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
        rows = RentDetails.query.update(self.toDict(), synchronize_session=False)
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
            RentDetails.rentDueDate: self.rentDueDate,
            RentDetails.baseRent: self.baseRent,
            RentDetails.rentMadePayableTo: self.rentMadePayableTo,
            RentDetails.parkingAmount: self.parkingAmount,
            RentDetails.parkingSpaces: self.parkingSpaces,
            RentDetails.houseId: self.houseId
        }

    def toJson(self):
        return {
            "rentDueDate": self.rentDueDate,
            "baseRent": self.baseRent,
            "rentMadePayableTo": self.rentMadePayableTo,
            "parkingAmount": self.parkingAmount,
            "parkingSpaces": self.parkingSpaces,
            "houseId": self.houseId
        }
    

    def __repr__(self):
        return "< Rent Details: " + str(self.baseRent) + " >"



class Amenity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    airConditioning = db.Column(db.Boolean())
    gas = db.Column(db.Boolean())
    guestParking = db.Column(db.Boolean())
    storage = db.Column(db.Boolean())
    onSiteLaundry = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), nullable=False)
    
    

    def __init__(self, **amenityData):
        self.airConditioning = amenityData.get("airConditioning", "") == "True"
        self.gas = amenityData.get("gas", "") == "True"
        self.guestParking = amenityData.get("guestParking", "") == "True"
        self.storage = amenityData.get("storage", "") == True
        self.onSiteLaundry = amenityData.get("onSiteLaundry", "") == "True"
        self.houseId = amenityData.get("houseId", "") == "True"
        


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
        rows = Amenity.query.update(self.toDict(), synchronize_session=False)
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
            Amenity.airConditioning: self.airConditioning,
            Amenity.gas: self.gas,
            Amenity.onSiteLaundry: self.onSiteLaundry,
            Amenity.storage: self.storage,
            Amenity.guestParking: self.guestParking,
            Amenity.houseId: self.houseId
        }

    def toJson(self):
        return [
                    {
                        "name": "Air Conditioning",
                        "includedInRent": self.airConditioning
                    },
                    {
                        "name": "Gas",
                        "includedInRent": self.gas
                    },
                    {
                        "name": "On Site Laundry",
                        "includedInRent": self.onSiteLaundry
                    },
                    {
                        "name": "Storage",
                        "includedInRent": self.storage
                    },
                    {
                        "name": "Guest Parking",
                        "includedInRent": self.guestParking
                    }
                ]
        
    

    def __repr__(self):
        return "<Amenity " + str(self.airConditioning) + " >"
        
class Utility(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    heat = db.Column(db.Boolean())
    electricity = db.Column(db.Boolean())
    water = db.Column(db.Boolean())
    internet = db.Column(db.Boolean())
    houseId = db.Column(db.Integer(), nullable=False)
    
    
    def __init__(self, **utilityData):
        self.heat = utilityData.get("heat", "") == "True"
        self.electricity = utilityData.get("electricity", "") == "True"
        self.water = utilityData.get("water", "") == "True"
        self.internet = utilityData.get("internet", "") == "True"
        self.houseId = utilityData.get("houseId", "") == "True"


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
        rows = Utility.query.update(self.toDict(), synchronize_session=False)
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
        return  {
            Utility.heat: self.heat,
            Utility.electricity: self.electricity,
            Utility.water: self.water,
            Utility.internet: self.internet,
            Utility.houseId: self.houseId
        }

    def toJson(self):
        return  [
                    {
                        "name": "Heat",
                        "responsibilityOf": "Tenant" if self.heat else "Homeowner"
                    },
                    {
                        "name": "Electricity",
                        "responsibilityOf": "Tenant" if self.electricity else "Homeowner"
                    },
                    {
                        "name": "Water",
                        "responsibilityOf": "Tenant" if self.water else "Homeowner"
                    },
                    {
                        "name": "Internet",
                        "responsibilityOf": "Tenant" if self.internet else "Homeowner"
                    }
                ]

   

    def __repr__(self):
        return "<Utility " + str(self.water) + " >"


class HomeownerLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100), )
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitNumber = db.Column(db.String(10))
    poBox = db.Column(db.String(10))
    homeownerId = db.Column(db.Integer(), nullable=False)
    houseId = db.Column(db.Integer(), nullable=False)

    def __init__(self, **homeownerLocationData):
        self.streetNumber = homeownerLocationData.get("streetNumber", "")
        self.streetName = homeownerLocationData.get("streetName", "")
        self.city = homeownerLocationData.get("city", "")
        self.province = homeownerLocationData.get("province", "")
        self.postalCode = homeownerLocationData.get("postalCode", "")
        self.unitNumber = homeownerLocationData.get("unitNumber", "")
        self.poBox = homeownerLocationData.get("poBox", "")
        self.homeownerId = homeownerLocationData.get("homeownerId", "")
        self.houseId = homeownerLocationData.get("houseId", "")

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
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def delete(self):
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).delete()
        db.session.commit()

    def toDict(self):
        return {
            HomeownerLocation.streetNumber: self.streetNumber,
            HomeownerLocation.streetName: self.streetName,
            HomeownerLocation.city: self.city,
            HomeownerLocation.province: self.province,
            HomeownerLocation.postalCode: self.postalCode,
            HomeownerLocation.unitNumber: self.unitNumber,
            HomeownerLocation.poBox: self.poBox
        }

    def toJson(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }

    def __repr__(self):
        return "< Homeowner Location: " + str(self.streetNumber) + " " + self.streetName + " >"