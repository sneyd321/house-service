from . import house
from flask import request, Response, jsonify, render_template, redirect
import json, requests
from server.api.forms import HomeownerLocationBasementForm, HomeownerLocationCondoForm, RentalUnitLocationForm, ArrangementForm
from server.api.models import House, HomeownerLocation, RentalUnitLocation
from server.api.RequestManager import Zookeeper, RequestManager
from server import app

zookeeper = Zookeeper()

def get_homeowner_gateway():
    return "192.168.0.108:8080"

def parse_token(request):
    bearer = request.headers.get("Authorization")
    if bearer:
        print(bearer, flush=True)
        return bearer[7:]
    return None

@house.route("House/<int:homeownerId>")
def get_house_form(homeownerId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        token = parse_token(request)
        if token:
            form = ArrangementForm()
            return render_template("Arrangement.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/" + "House", token=token)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Zookeeper down", status=503)
    

@house.route("House/<int:homeownerId>", methods=["POST"])
def create_house(homeownerId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = ArrangementForm(request.form)
        if form.validate():
            house = House(homeownerId, **request.form)
            if house.insert():
                return Response(response="HomeownerLocation/" + house.province + "/" + house.arrangement + "/" + str(homeownerId) + "/" + str(house.id), status=201)
            return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: House failed to save")
        return render_template("Arrangement.html", form=form, fields=list(form._fields.values()), conflict="Error", url="http://" + service + "/homeowner-gateway/v1/" + "House")
    return Response(response="Error: Zookeeper down", status=503)
    

@house.route("HomeownerLocation/<string:province>/<string:arrangement>/<int:homeownerId>/<int:houseId>")
def get_homeowner_location_form(province, arrangement, homeownerId, houseId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        if arrangement == "Basement":
            form = HomeownerLocationBasementForm()
            return render_template("OntarioHomeownerLocation.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/" + province + "/" + arrangement + "/" + str(homeownerId) + "/" + str(houseId))
        if arrangement == "Condo":
            form = HomeownerLocationCondoForm()
            return render_template("OntarioHomeownerLocation.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/" + province + "/" + arrangement + "/" + str(homeownerId) + "/" + str(houseId))
        return Response(response="Error: House arrangement not specified", status=400) 
    return Response(response="Error: Zookeeper down", status=503)



@house.route("HomeownerLocation/Ontario/Basement/<int:homeownerId>/<int:houseId>", methods=["POST"])
def create_homeowner_location_basement(homeownerId, houseId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = HomeownerLocationBasementForm(request.form)
        attrs = list(form._fields.values())
        if form.validate_on_submit():
            homeownerLocation = HomeownerLocation(province="Ontario", homeownerId=homeownerId, houseId=houseId, **request.form)
            if homeownerLocation.insert():
                rentalUnitLocation = RentalUnitLocation(province="Ontario", houseId=houseId, unitName="Basement", isCondo=False, **request.form)
                if rentalUnitLocation.insert():
                    return Response(response="HouseComplete/" + str(houseId), status=201)
                return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="Error: Adding rental unit location", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/Ontario/Basement/" + str(homeownerId) + "/" + str(houseId))
            return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="Error: Adding homeowner location", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/Ontario/Basement/" + str(homeownerId) + "/" + str(houseId))
        return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/Ontario/Basement/" + str(homeownerId) + "/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
    


@house.route("HomeownerLocation/Ontario/Condo/<int:homeownerId>/<int:houseId>", methods=["POST"])
def create_homeowner_location_condo(homeownerId, houseId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = HomeownerLocationCondoForm(request.form)
        attrs = list(form._fields.values())
        if form.validate_on_submit():

            homeownerLocation = HomeownerLocation(province="Ontario", homeownerId=homeownerId, houseId=houseId, **request.form)
            if homeownerLocation.insert():
                return Response(response="RentalUnitLocation/Ontario/" + str(houseId), status=201)
            return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="Error: Adding homeowner location", url="http://" + service + "/HomeownerLocation/Ontario/Condo/" + str(homeownerId) + "/" + str(houseId))
        return render_template("OntarioHomeownerLocation.html", form=form, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/HomeownerLocation/Ontario/Condo/" + str(homeownerId) + "/" + str(houseId))

    return Response(response="Error: Zookeeper down", status=503)
    



@house.route("RentalUnitLocation/Ontario/<int:houseId>")
def get_rental_unit_basement_location(houseId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = RentalUnitLocationForm()
        return render_template("OntarioRentalUnitLocation.html", form=form, fields=list(form._fields.values()), conflict="", url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
    


@house.route("RentalUnitLocation/Ontario/<int:houseId>", methods=["POST"])
def create_rental_unit_basement_location(houseId):
    global zookeeper
    service = zookeeper.get_service("homeowner-gateway")
    service = get_homeowner_gateway()
    if service:
        form = RentalUnitLocationForm(request.form)
        attrs = list(form._fields.values())
        if form.validate():
            rentalUnitLocation = RentalUnitLocation(houseId=houseId, isCondo=True, province="Ontario", unitName="Rental Unit", **request.form)
            if rentalUnitLocation.insert():
                return Response(response="HouseComplete/" + str(houseId), status=201)
            return render_template("RentalUnitLocation.html", form=form, fields=attrs, conflict="Error: Failed to create rental unit location", url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/" + str(houseId))
        return render_template("OntarioRentalUnitLocation.html", form=form, fields=attrs, conflict="", url="http://" + service + "/homeowner-gateway/v1/RentalUnitLocation/Ontario/" + str(houseId))
    return Response(response="Error: Zookeeper down", status=503)
    
   


@house.route("HouseComplete/<int:houseId>", methods=["POST"])
def house_complete(houseId):
    house = House.query.get(houseId)
    house.isComplete = True
    if house.update():
        return Response(response="FormComplete", status=201)
    return Response(response="Error: Failed to update", status=409)



##############################################################################################################################################

    

@house.route("Homeowner/<int:id>/House")
def get_houses(id):
    houses = House.query.filter(House.homeownerId == id).filter(House.isComplete == True).all()
    if houses:
        print([house.toJson() for house in houses])


        return jsonify([house.toJson() for house in houses])
    return Response(response="Error: No houses with homeowner id: " + str(id), status=404)


@house.route("House/<int:houseId>/Tenant")
def get_house(houseId):
    house = House.query.get(houseId)
    if house:
        return jsonify(house.toJson())
    return Response(response="Error: No house with house id: " + str(houseId), status=404)







