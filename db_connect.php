<?php

class database 
{
    var $host = "localhost";
    var $username = "root";
    var $password = "Sautmanurung234";
    var $database = "booking-app-database";
    var $koneksi;

    function __construct()
    {
        $this->koneksi = mysqli_connect($this->host, $this->username, $this->password, $this->database);
    }
}