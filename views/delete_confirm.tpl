<!-- views/delete_confirm.tpl -->
<p>Are you sure you want to delete the car rental for "{{ row[2] }}" with car model "{{ row[1] }}"?</p>
<form action="/delete/{{ row[0] }}" method="post">
    <input type="submit" value="Yes">
</form>
<a href="/">No, go back</a>
