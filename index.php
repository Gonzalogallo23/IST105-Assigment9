<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route with OpenRouteService</title>
</head>
<body>
    <h2>Enter Origin and Destination</h2>
    <form action="process.php" method="post">
        <label for="orig">Origin Location:</label>
        <input type="text" id="orig" name="orig" required>
        <br><br>
        <label for="dest">Destination Location:</label>
        <input type="text" id="dest" name="dest" required>
        <br><br>
        <button type="submit">Calculate Route</button>
    </form>
</body>
</html>