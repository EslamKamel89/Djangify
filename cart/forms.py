from django import forms

from store.models import Product


class UpdateCartItemForm(forms.Form):
    product_id = forms.IntegerField(min_value=1)
    quantity = forms.IntegerField(min_value=1, initial=1)
    action = forms.ChoiceField(choices=[("inc", "Increase"), ("dec", "Decrease")])
    product: Product

    def clean_product_id(self):
        product_id = self.cleaned_data["product_id"]

        self.product = Product.objects.filter(
            id=product_id,
            is_available=True,
        ).first()  # type: ignore
        if not self.product:
            raise forms.ValidationError("Invalid product")
        return product_id
