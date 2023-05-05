from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetClinics.db"
db = SQLAlchemy(app)


# Store all the clinics' info in English
class VetClinicsEN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    website = db.Column(db.String)
    note = db.Column(db.String)
    phone = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __repr__(self):
        return self.name


# Store all the clinics' info in Chinese
class VetClinicsZH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    website = db.Column(db.String)
    note = db.Column(db.String)
    phone = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __repr__(self):
        return self.name


clinicFieldsEN = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
    "address": fields.String,
    "website": fields.String,
    "note": fields.String,
    "phone": fields.String,
    "lat": fields.Fixed,
    "lng": fields.Fixed,
}

clinicFieldsZH = {
    "id": fields.Integer,
    "name": fields.String,
    "location": fields.String,
    "address": fields.String,
    "website": fields.String,
    "note": fields.String,
    "phone": fields.String,
    "lat": fields.Fixed,
    "lng": fields.Fixed,
}


class ClinicsEN(Resource):
    # get all the vet clinic (en): DONE
    @marshal_with(clinicFieldsEN)
    def get(self):
        all_clinics_en = VetClinicsEN.query.all()
        return all_clinics_en

    # add new vet clinic (en): DONE
    @marshal_with(clinicFieldsEN)
    def post(self):
        data = request.json

        # ERROR: Object of type VetClinics is not JSON serializable(SOLVED after marshal_with decorator is added)
        clinic = VetClinicsEN(
            name=data["name"],
            address=data["address"],
            location=data["location"],
            website=data["website"],
            note=data["note"],
            phone=data["phone"],
            lat=data["lat"],
            lng=data["lng"],
        )
        db.session.add(clinic)
        db.session.commit()
        clinics = VetClinicsEN.query.all()

        return clinics


class ClinicsZH(Resource):
    # get all the vet clinic (zh): DONE
    @marshal_with(clinicFieldsZH)
    def get(self):
        all_clinics_en = VetClinicsZH.query.all()
        return all_clinics_en

    # add new vet clinic (zh): DONE
    # ISSUE: works fine, but it showed Chinese as ascii code...
    @marshal_with(clinicFieldsZH)
    def post(self):
        data = request.json

        # ERROR: Object of type VetClinics is not JSON serializable(SOLVED after marshal_with decorator is added)
        clinic = VetClinicsZH(
            name=data["name"],
            address=data["address"],
            location=data["location"],
            website=data["website"],
            note=data["note"],
            phone=data["phone"],
            lat=data["lat"],
            lng=data["lng"],
        )
        db.session.add(clinic)
        db.session.commit()
        clinics = VetClinicsZH.query.all()

        return clinics


# DONE
class ClinicEN(Resource):
    # get single vet clinic's info (en): DONE
    @marshal_with(clinicFieldsEN)
    def get(self, pk):
        clinic = VetClinicsEN.query.filter_by(id=pk).first()
        return clinic


    # update vet clinic info (en): DONE
    @marshal_with(clinicFieldsEN)
    def put(self, pk):
        data = request.json
        clinic = VetClinicsEN.query.filter_by(id=pk).first()
        clinic.name = data["name"]
        clinic.address = data["address"]
        clinic.location = data["location"]
        clinic.website = data["website"]
        clinic.note = data["note"]
        clinic.phone = data["phone"]
        clinic.lat = data["lat"]
        clinic.lng = data["lng"]
        db.session.commit()

        return clinic

    
    # delete vet clinic info (en): DONE
    @marshal_with(clinicFieldsEN)
    def delete(self, pk):
        clinic = VetClinicsEN.query.filter_by(id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsEN.query.all()
        return clinics


class ClinicZH(Resource):

    # get single vet clinic's info (zh): DONE
    @marshal_with(clinicFieldsZH)
    def get(self, pk):
        clinic = VetClinicsZH.query.filter_by(id=pk).first()
        return clinic


    # delete vet clinic info (zh): DONE
    @marshal_with(clinicFieldsZH)
    def delete(self, pk):
        clinic = VetClinicsZH.query.filter_by(id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsZH.query.all()
        return clinics

    # update vet clinic info (zh): DONE
    @marshal_with(clinicFieldsZH)
    def put(self, pk):
        data = request.json
        clinic = VetClinicsZH.query.filter_by(id=pk).first()
        clinic.name = data["name"]
        clinic.address = data["address"]
        clinic.location = data["location"]
        clinic.website = data["website"]
        clinic.note = data["note"]
        clinic.phone = data["phone"]
        clinic.lat = data["lat"]
        clinic.lng = data["lng"]
        db.session.commit()

        return clinic


class ClinicsFromLocationEN(Resource):
    # get all vet clinics according to search location (en): DONE
    @marshal_with(clinicFieldsEN)
    def get(self, search_location):
        clinics = VetClinicsEN.query.filter_by(location=search_location).all()
        return clinics


class ClinicsFromLocationZH(Resource):
    # get all vet clinics according to search location (zh): DONE
    @marshal_with(clinicFieldsZH)
    def get(self, search_location):
        clinics = VetClinicsZH.query.filter_by(location=search_location).all()
        return clinics


class ClinicFromLocationEN(Resource):
    # get single vet clinic according to search location and id (en): DONE
    @marshal_with(clinicFieldsEN)
    def get(self, search_location, pk):
        clinic = VetClinicsEN.query.filter_by(location=search_location, id=pk).first()
        return clinic
    
    # update vet clinic info (en): DONE
    @marshal_with(clinicFieldsEN)
    def put(self, search_location, pk):
        data = request.json
        clinic = VetClinicsEN.query.filter_by(location=search_location, id=pk).first()
        clinic.name = data["name"]
        clinic.address = data["address"]
        clinic.location = data["location"]
        clinic.website = data["website"]
        clinic.note = data["note"]
        clinic.phone = data["phone"]
        clinic.lat = data["lat"]
        clinic.lng = data["lng"]
        db.session.commit()

        return clinic

    
    # delete vet clinic info (en): DONE
    @marshal_with(clinicFieldsEN)
    def delete(self, search_location, pk):
        clinic = VetClinicsEN.query.filter_by(location=search_location, id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsEN.query.all()
        return clinics


class ClinicFromLocationZH(Resource):
    # get single vet clinic according to search location and id (zh): DONE
    @marshal_with(clinicFieldsZH)
    def get(self, search_location, pk):
        clinic = VetClinicsZH.query.filter_by(location=search_location, id=pk).first()
        return clinic
    
     # delete vet clinic info (zh): DONE
    @marshal_with(clinicFieldsZH)
    def delete(self, search_location, pk):
        clinic = VetClinicsZH.query.filter_by(location=search_location,id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsZH.query.all()
        return clinics

    # update vet clinic info (zh): DONE
    @marshal_with(clinicFieldsZH)
    def put(self, search_location, pk):
        data = request.json
        clinic = VetClinicsZH.query.filter_by(location=search_location, id=pk).first()
        clinic.name = data["name"]
        clinic.address = data["address"]
        clinic.location = data["location"]
        clinic.website = data["website"]
        clinic.note = data["note"]
        clinic.phone = data["phone"]
        clinic.lat = data["lat"]
        clinic.lng = data["lng"]
        db.session.commit()

        return clinic


api.add_resource(ClinicsEN, "/v2/clinics/en")
api.add_resource(ClinicsZH, "/v2/clinics/zh")
api.add_resource(ClinicEN, "/v2/clinics/en/<int:pk>")
api.add_resource(ClinicZH, "/v2/clinics/zh/<int:pk>")
api.add_resource(ClinicsFromLocationEN, "/v2/clinics/en/<search_location>")
api.add_resource(ClinicsFromLocationZH, "/v2/clinics/zh/<search_location>/")
api.add_resource(ClinicFromLocationEN, "/v2/clinics/en/<search_location>/<int:pk>")
api.add_resource(ClinicFromLocationZH, "/v2/clinics/zh/<search_location>/<int:pk>")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
