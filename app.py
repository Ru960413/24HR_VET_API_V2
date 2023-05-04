from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vetClinics.db"
db = SQLAlchemy(app)


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
    # DONE
    @marshal_with(clinicFieldsEN)
    def get(self):
        all_clinics_en = VetClinicsEN.query.all()
        return all_clinics_en

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
    # DONE
    @marshal_with(clinicFieldsZH)
    def get(self):
        all_clinics_en = VetClinicsZH.query.all()
        return all_clinics_en

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
    # For getting a vet clinic's info
    @marshal_with(clinicFieldsEN)
    def get(self, pk):
        clinic = VetClinicsEN.query.filter_by(id=pk).first()
        return clinic

    # DONE
    # For updating vet clinic info
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

    # DONE
    # For deleting vet clinic info
    @marshal_with(clinicFieldsEN)
    def delete(self, pk):
        clinic = VetClinicsEN.query.filter_by(id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsEN.query.all()
        return clinics


class ClinicZH(Resource):
    # DONE
    # For getting a vet clinic's info
    @marshal_with(clinicFieldsZH)
    def get(self, pk):
        clinic = VetClinicsZH.query.filter_by(id=pk).first()
        return clinic

    # DONE
    # For deleting vet clinic info
    @marshal_with(clinicFieldsZH)
    def delete(self, pk):
        clinic = VetClinicsZH.query.filter_by(id=pk).first()
        db.session.delete(clinic)
        db.session.commit()

        clinics = VetClinicsZH.query.all()
        return clinics
    
    # DONE
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


class ClinicsLocationEN(Resource):
    pass
    # @marshal_with(clinicFieldsEN)
    # def get(self, location, pk):

    #     clinic = VetClinicsEN.query.filter_by(id=pk, location=location).first()
    #     return clinic


class ClinicsLocationZH(Resource):
    pass


api.add_resource(ClinicsEN, "/api/v2/en")
api.add_resource(ClinicsZH, "/api/v2/zh")
api.add_resource(ClinicEN, "/api/v2/en/<int:pk>")
api.add_resource(ClinicZH, "/api/v2/zh/<int:pk>")
# api.add_resource(ClinicsLocationEN, "/api/v2/en/<str: location>/")
# api.add_resource(ClinicsLocationZH, "/api/v2/zh/{location}/")
# api.add_resource(ClinicEN, "/api/v2/en/{location}/<int:pk>")
# api.add_resource(ClinicZH, "/api/v2/zh/{location}/<int:pk>")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
