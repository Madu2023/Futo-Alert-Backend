<?php
// connection.php - This file handles the database connection

// Database configuration
$host = 'localhost';        // Hostname of your MySQL server (usually localhost)
$dbname = 'Myobinna_db';    // Name of your database
$username = 'db_user';      // Replace with your database username
$password = 'db_password';  // Replace with your database password

try {
    // Create a PDO instance for MySQL database connection
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // Set the PDO error mode to exception for better error handling
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Uncomment this line to confirm the connection is successful
    // echo "Connected to the database successfully!";
} catch (PDOException $e) {
    // In case of error, print a message and stop the script
    echo "Connection failed: " . $e->getMessage();
    exit;
}
?>
