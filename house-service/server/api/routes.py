from . import house
from flask import request, Response, jsonify, render_template, redirect
import json, requests
from server.api.forms import RentalUnitCondoForm, RentalUnitLocationForm, ArrangementForm
from server.api.models import House, RentalUnitLocation
from server.api.RequestManager import Zookeeper, RequestManager
from server import app

zookeeper = Zookeeper()

def get_homeowner_gateway():
    return "34.107.132.144"

def parse_token(request):
    bearer = request.headers.get("Authorization")
    if bearer:
        print(bearer, flush=True)
        return bearer[7:]
    return None

@house.route("House/<int:homeownerId>")
def get_house_form(homeownerId):
    service = get_homeowner_gateway()
  
    form = ArrangementForm()
    return render_template("Arrangement.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/House/" + str(homeownerId))


@house.route("House/<int:homeownerId>", methods=["POST"])
def create_house(homeownerId):
    service = get_homeowner_gateway()
    #Validate form
    print(request.form)
    form = ArrangementForm(request.form)
    attrs = list(form._fields.values())
    
    
    if not request.form or "arrangement" not in request.form or "province" not in request.form:
        return render_template("Arrangement.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/House/" + str(homeownerId))
    
    #Insert house
    house = House(homeownerId, **request.form)
    if not house.insert():
        return render_template("RentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: House failed to save")

    houseId = house.id
    arangement = house.arrangement
    house.close_session()

    return Response(response="RentalUnitLocation/Ontario/" + arangement + "/" + str(houseId), status=201)

    
    
    
    
@house.route("RentalUnitLocation/Ontario/<string:rentalType>/<int:houseId>")
def get_rental_unit_basement_location(rentalType, houseId):
    service = get_homeowner_gateway()
    form = RentalUnitLocationForm()
    if rentalType == "Condo":
        form = RentalUnitCondoForm()
    return render_template("OntarioRentalUnitLocation.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/" + rentalType + "/" + str(houseId))

    


@house.route("RentalUnitLocation/Ontario/Basement/<int:houseId>", methods=["POST"])
def create_rental_unit_basement_location(houseId):

    service = get_homeowner_gateway()
   
    form = RentalUnitLocationForm(request.form)
    attrs = list(form._fields.values())
    if not request.form or "streetNumber" not in request.form or "streetName" not in request.form or "city" not in request.form or "postalCode" not in request.form:
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Basement/" + str(houseId))

    if not form.validate():
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Basement/" + str(houseId))

    rentalUnitLocation = RentalUnitLocation(houseId=houseId, isCondo=True, province="Ontario", unitName="Basement", **request.form)
    if not rentalUnitLocation.insert():
        return render_template("RentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Failed to create rental unit location", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Basement/" + str(houseId))
    
    return Response(response="HouseComplete/" + str(houseId), status=201)


@house.route("RentalUnitLocation/Ontario/Condo/<int:houseId>", methods=["POST"])
def create_rental_unit_condo_location(houseId):
  
    service = get_homeowner_gateway()
  
    form = RentalUnitCondoForm(request.form)
    attrs = list(form._fields.values())
    if not request.form or "streetNumber" not in request.form or "streetName" not in request.form or "city" not in request.form or "postalCode" not in request.form or "unitNumber" not in request.form:
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Condo/" + str(houseId))

    if not form.validate():
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Condo/" + str(houseId))

    unitNumber = request.form["unitNumber"]
    rentalUnitLocation = RentalUnitLocation(houseId=houseId, isCondo=True, province="Ontario", unitName="Unit " + str(unitNumber), **request.form)
    if not rentalUnitLocation.insert():
        return render_template("RentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Failed to create rental unit location", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/Condo/" + str(houseId))
    
    return Response(response="HouseComplete/" + str(houseId), status=201)



@house.route("RentalUnitLocation/Ontario/House/<int:houseId>", methods=["POST"])
def create_rental_unit_house_location(houseId):
   
    service = get_homeowner_gateway()
   
    form = RentalUnitLocationForm(request.form)
    attrs = list(form._fields.values())
    if not request.form or "streetNumber" not in request.form or "streetName" not in request.form or "city" not in request.form or "postalCode" not in request.form:
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Invalid Request Data", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/House/" + str(houseId))

    if not form.validate():
        return render_template("OntarioRentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/House/" + str(houseId))

    rentalUnitLocation = RentalUnitLocation(houseId=houseId, isCondo=False, province="Ontario", unitName="Rental Unit", **request.form)
    if not rentalUnitLocation.insert():
        return render_template("RentalUnitLocation.html", 
        form=form, 
        fields=attrs, 
        conflict="Error: Failed to create rental unit location", 
        url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/House/" + str(houseId))
    
    return Response(response="HouseComplete/" + str(houseId), status=201)


@house.route("HouseComplete/<int:houseId>", methods=["POST"])
def house_complete(houseId):
    house = House.query.get(houseId)
    house.isComplete = True
    if house.update():
        return Response(response="FormComplete", status=201)
    return Response(response="Error: Failed to update", status=409)



##############################################################################################################################################

    

@house.route("Homeowner/<int:homeownerId>/House")
def get_houses(homeownerId):
    houses = House.query.filter(House.homeownerId == homeownerId).filter(House.isComplete == True).all()
    return jsonify([house.toJson() for house in houses])
       

@house.route("House/<int:houseId>/Tenant")
def get_house(houseId):
    house = House.query.get(houseId)
    if house:
        return jsonify(house.toJson())
    return Response(response="House Not Found", status=404)

   






