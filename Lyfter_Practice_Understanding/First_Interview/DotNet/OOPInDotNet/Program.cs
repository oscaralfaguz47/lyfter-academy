using DotNet.OOPInDotNet;

// Top-level statements: the modern entry point. The compiler generates the Main method for you.

// Local variables use camelCase.
var parentClassInstanceArgument = new Info(
    "Parent class instance attribute",
    "I'm an argument passed to the constructor. Oscar created me, and my whole value will " +
    "be stored in the parent class instance attribute and the child classes will reuse me.");

var parentClassProtectedInstanceArgument = new Info(
    "Parent class PROTECTED instance attribute",
    "I'm a protected argument passed to the constructor, only this class and its children can use me.");

var parentClassPrivateInstanceArgument = new Info(
    "Parent class PRIVATE instance attribute",
    "I'm a private argument passed to the constructor, but I cannot be accessed directly, only through my property.");

var childClassInstanceArgument = new Info(
    "Child class instance attribute",
    "I'm an argument passed to the constructor. Oscar created me, and my whole value will " +
    "be stored in the child class instance attribute.");

var childClassProtectedInstanceArgument = new Info(
    "Child class PROTECTED instance attribute",
    "I'm a protected argument passed to the constructor, only this class and its children can use me.");

var childClassPrivateInstanceArgument = new Info(
    "Child class PRIVATE instance attribute",
    "I'm a private argument passed to the constructor, but I cannot be accessed directly, only through my property.");

// An object is an instance of a class. 'new' calls the constructor.
var myParentObject = new MyParentClass(
    parentClassInstanceArgument,
    parentClassProtectedInstanceArgument,
    parentClassPrivateInstanceArgument);

var myChildObject = new MyChildClass(
    parentClassInstanceArgument,
    childClassProtectedInstanceArgument,
    childClassPrivateInstanceArgument,
    childClassInstanceArgument);

Console.WriteLine("-------------- PARENT CLASS ------------------------");
Console.WriteLine($"I'm an object based on the class: {myParentObject.GetType().Name}");
myParentObject.MyInstanceMethod();
MyParentClass.MyStaticMethod(); // Static: called through the CLASS. myParentObject.MyStaticMethod() doesn't compile.
Console.WriteLine();

Console.WriteLine("-------------- CHILD CLASS (INHERITANCE) ------------------------");
Console.WriteLine($"I'm an object based on the class: {myChildObject.GetType().Name}");
myChildObject.MyInstanceMethod();

// No MRO in C#: the chain is always a straight line (one base class per class).
var inheritanceChain = new List<string>();
for (Type? type = typeof(MyChildClass); type is not null; type = type.BaseType)
{
    inheritanceChain.Add(type.Name);
}

var implementedInterfaces = typeof(MyChildClass).GetInterfaces().Select(i => i.Name);
Console.WriteLine($"Inheritance chain: {string.Join(" -> ", inheritanceChain)}");
Console.WriteLine($"Implemented interfaces: {string.Join(", ", implementedInterfaces)}");
Console.WriteLine();

Console.WriteLine("-------------- ABSTRACTION ------------------------");
myChildObject.MyAbstractedMethod();

// In Python this fails at runtime (TypeError). In C# it doesn't even compile (error CS0144):
// var abstraction = new IMyAbstractParent();
Console.WriteLine("Can't instantiate an interface: that line doesn't even compile (error CS0144).");

// What you CAN do is use the object through its abstraction: you only see WHAT it does.
IMyAbstractParent abstraction = myChildObject;
abstraction.MyAbstractedMethod();
Console.WriteLine();

Console.WriteLine("-------------- POLYMORPHISM ------------------------");
MyParentClass[] objects = [myParentObject, myChildObject];
foreach (var obj in objects)
{
    obj.MyPolymorphicMethod(); // Same call, different behavior
}

Console.WriteLine();

Console.WriteLine("-------------- ENCAPSULATION ------------------------");

// PRIVATE data, read and changed from outside only through its public property.
Console.WriteLine($"Read through the public property: '{myChildObject.PrivateParentInstanceAttribute.Name}'");

// The setter rejects invalid values
try
{
    myChildObject.PrivateParentInstanceAttribute = new Info(
        "Invalid value",
        "This description doesn't have the keyword.");
}
catch (ArgumentException error)
{
    Console.WriteLine($"Setter validation worked: {error.Message}");
}

// The setter accepts a valid value
myChildObject.PrivateParentInstanceAttribute = new Info(
    "Updated PRIVATE instance attribute",
    "I was updated through the setter of my private field.");
Console.WriteLine($"Updated through the setter: '{myChildObject.PrivateParentInstanceAttribute.Name}'");

// PROTECTED data, only the class and its children can use it.
myChildObject.ShowProtectedAccess();
myChildObject.UpdateProtectedAttribute(new Info(
    "Updated PROTECTED instance attribute",
    "I was updated by the child through the protected setter."));
myChildObject.ShowProtectedAccess();

// From outside the class hierarchy, these lines don't compile (error CS0122):
// Console.WriteLine(myChildObject.ProtectedParentInstanceAttribute);
// Console.WriteLine(myChildObject._privateParentInstanceAttribute);
Console.WriteLine("Direct access to protected/private members from outside doesn't compile (error CS0122), as expected.");