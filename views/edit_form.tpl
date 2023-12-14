<!-- views/edit_form.tpl -->
<form action="/edit/{{ row[0] }}" method="post">
    Car Model: <input type="text" name="car_model" value="{{ row[1] }}" required><br>
    <input type="submit" value="Update Car Rental">
</form>
