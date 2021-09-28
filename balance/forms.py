from flask_wtf import FlaskForm
from wtforms import DateField,HiddenField, FloatField, RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, NumberRange
import datetime

def validar_fecha(formulario, campo):
    hoy = datetime.date.today()

    if campo.data > hoy:
        raise ValidationError("La fecha no puede ser posterior a hoy")

class MovimientoFormulario(FlaskForm):

    id = HiddenField()
    fecha = DateField("Fecha", validators = [DataRequired(message="Debe informar la fecha")])
    concepto = StringField("Concepto", validators=[DataRequired(message="Debe informar el concepto"), Length(min=10)])
    cantidad = FloatField("cantidad", validators=[DataRequired(message="Debe informar el monto"), NumberRange(min=0.01)])

    ingreso_gasto = RadioField(validators=[DataRequired("Debe informar el tipo de movimiento")],
                                            choices=[("G","Gasto"),("I","Ingreso")])

    submit = SubmitField("Aceptar")

    def validate_fecha(self, campo):
        hoy = datetime.date.today()
        if campo.data > hoy:
            raise ValidationError("La fecha no puede ser posterior a hoy")
