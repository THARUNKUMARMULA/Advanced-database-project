<!-- views/index.tpl -->
<form action="/" method="get">
    Search Customer: <input type="text" name="search" placeholder="Enter customer name">
    <input type="submit" value="Search">
</form>

    <h2>Search Results:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Car Model</th>
            <th>Customer Name</th>
            <th>Customer Email</th>
            <th>Edit</th>
            <th>Delete</th>
        </tr>
        % for row in rows:
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td><a href="/edit/{{ row[0] }}">Edit</a></td>
                <td><a href="/delete/{{ row[0] }}">Delete</a></td>
            </tr>
        % end
    </table>
<br>
<a href="/add">Rent a Car</a>
