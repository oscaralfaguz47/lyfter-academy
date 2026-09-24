namespace DotNet.OOPInDotNet;

// ABSTRACTION with an interface
// An interface shows WHAT a class must do, but not HOW. It can't be instantiated.
// Any class that implements it is FORCED by the compiler to implement all its members.
// Naming convention: interfaces start with I + PascalCase.
//
// C# also has abstract classes (the closest thing to Python's ABC):
//     public abstract class Shape { public abstract double Area(); }
// They can have fields, constructors and implemented methods, BUT a class can inherit
// from only ONE class. So for a "second parent" we use an interface: a class can
// implement as many interfaces as it wants.
public interface IMyAbstractParent
{
    void MyAbstractedMethod(); // No body: implementing classes have to provide the logic
}