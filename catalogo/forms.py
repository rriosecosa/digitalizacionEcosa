from django import forms

from .models import ProductoCatalogo


class ProductoCatalogoForm(forms.ModelForm):

    class Meta:

        model = ProductoCatalogo

        fields = [

            'imagen_catalogo',
            'referencia',
            'descripcion_catalogo',
            'especificaciones',
            'orden_catalogo',
            'visible_catalogo'

        ]

        widgets = {

            'referencia': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'descripcion_catalogo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),

            'especificaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 8
                }
            ),

            'orden_catalogo': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'visible_catalogo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }