<?php
// Define variables to hold form data and error messages
$name = $email = $gender = "";
$nameErr = $emailErr = $genderErr = "";

// Process the form when it's submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Validate name
    if (empty($_POST["name"])) {
        $nameErr = "Name is required";
    } else {
        $name = test_input($_POST["name"]);
    }
    
    // Validate email
    if (empty($_POST["email"])) {
        $emailErr = "Email is required";
    } else {
        $email = test_input($_POST["email"]);
        // Check if the email format is valid
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $emailErr = "Invalid email format";
        }
    }
    
    // Validate gender
    if (empty($_POST["gender"])) {
        $genderErr = "Gender is required";
    } else {
        $gender = test_input($_POST["gender"]);
    }
}

// Function to clean and sanitize input data
function test_input($data) {
    $data = trim($data); // Remove unnecessary whitespace
    $data = stripslashes($data); // Remove backslashes
    $data = htmlspecialchars($data); // Convert special characters to HTML entities
    return $data;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Form Control Example</title>
</head>
<body>

<h2>PHP Form Control Example</h2>
<p><span style="color:red;">* required field</span></p>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
    Name: <input type="text" name="name" value="<?php echo $name;?>">
    <span style="color:red;">* <?php echo $nameErr;?></span>
    <br><br>
    
    Email: <input type="text" name="email" value="<?php echo $email;?>">
    <span style="color:red;">* <?php echo $emailErr;?></span>
    <br><br>
    
    Gender:
    <input type="radio" name="gender" value="male" <?php if (isset($gender) && $gender == "male") echo "checked";?>> Male
    <input type="radio" name="gender" value="female" <?php if (isset($gender) && $gender == "female") echo "checked";?>> Female
    <span style="color:red;">* <?php echo $genderErr;?></span>
    <br><br>
    
    <input type="submit" value="Submit">
</form>

<?php
// Display the data after submission if there are no errors
if ($_SERVER["REQUEST_METHOD"] == "POST" && empty($nameErr) && empty($emailErr) && empty($genderErr)) {
    echo "<h2>Your Input:</h2>";
    echo "Name: " . $name . "<br>";
    echo "Email: " . $email . "<br>";
    echo "Gender: " . $gender . "<br>";
}
?>

</body>
</html>
