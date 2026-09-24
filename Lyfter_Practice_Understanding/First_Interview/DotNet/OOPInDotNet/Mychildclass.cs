namespace DotNet.OOPInDotNet;

// INHERITANCE
// C# allows ONE base class + any number of interfaces.
// There's no multiple class inheritance, so there's no MRO to worry about.
//
// 'sealed': nobody can inherit from this class. Good practice for classes
// that weren't designed to be extended.
public sealed class MyChildClass : MyParentClass, IMyAbstractParent
{
    // ': base(...)' runs the parent's constructor first, like super().__init__()
    public MyChildClass(
        Info publicParameter,
        Info protectedParameter,
        Info privateParameter,
        Info childParameter)
        : base(publicParameter, protectedParameter, privateParameter)
    {
        PublicChildInstanceAttribute = childParameter;
    }

    public Info PublicChildInstanceAttribute { get; set; }

    // Overrides and extends the parent's version. 'base' is the equivalent of super().
    public override void MyInstanceMethod()
    {
        base.MyInstanceMethod();
        Console.WriteLine("I override my parent's method, reuse its behavior with base, and add my own.");
    }

    // Overrides the parent's version (polymorphism). 'override' is mandatory.
    public override void MyPolymorphicMethod()
    {
        Console.WriteLine("I'm the CHILD'S version of MyPolymorphicMethod(), I override my parent's.");
    }

    // Implements the method required by IMyAbstractParent.
    // No 'override' here: interface members are implemented, not overridden.
    public void MyAbstractedMethod()
    {
        Console.WriteLine("I'm implementing the logic of MyAbstractedMethod() that IMyAbstractParent doesn't implement.");
    }

    // Protected in action: a child CAN use the parent's protected property...
    public void ShowProtectedAccess()
    {
        Console.WriteLine($"As a child, I can read the protected property: '{ProtectedParentInstanceAttribute.Name}'");

        // ...but NOT the parent's private field. This line doesn't compile (error CS0122):
        // Console.WriteLine(_privateParentInstanceAttribute.Name);
    }

    // The child changes the protected property, and the parent's setter still validates it.
    public void UpdateProtectedAttribute(Info newValue)
    {
        ProtectedParentInstanceAttribute = newValue;
    }
}