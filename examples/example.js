function greet(name) {
    var greeting = "Hello, " + name + "!";
    console.log(greeting);
}

function add(a, b) {
    var sum = a + b;
    console.log("Sum: " + sum);
    return sum;
}

function multiply(a, b) {
    var product = a * b;
    console.log("Product: " + product);
    return product;
}

greet("World");
add(5, 3);
multiply(4, 7);