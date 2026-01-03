<!-- introduction to php
 <?php
    echo "Hello, World!";
    // php variables example
    $name =  "John Doe";
    $age = 30;
    $developer = true;
    echo "Name: " . $name . ", Age: " . $age . ", Developer: " . ($developer ? "Yes" : "No");

    // arrays in php
    $colors = ["Red", "Green", "Blue"];
    echo $colors[1];
    // associative arrays in php
    $user = [
        "name" => "deborah" , 
        "age" =>19 ,
         "email" => "dez@mail.com"
        ];
        echo "user_name:" . $user["name"];
        // conditals in php
        if ($age>18){
            echo "adult" ;
        } else {
            echo "minor" ;
        }
        // loops in php
        for ($i=0; $i<5; $i++){
            echo "Numb: " . $i ;
        }
        $numbers = [1, 2, 3, 4, 5];
        foreach ($numbers as $num){
            echo "Number: " . $num;
        }
        // functions in php
        function greet($devs){
            return "hello, " . $devs . "!";
        }
        echo greet("deborah"); 
        // classes and oop in php
        class User{
            public $name;
            public $age;
            //constructor
            public function __construct($name , $age){
                $this -> name = $name;
                $this -> age  = $age;
            }
            //method
            public function introduce(){
                return "Hi, I'm " . $this->name . " and I'm " . $this->age . " years old.";
            }
            

        }
        $new_user = new User("deborah" , 37);
            echo $new_user -> introduce();