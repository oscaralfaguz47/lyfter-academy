namespace DotNet.OOPInDotNet;

// A class is a blueprint from which objects are created.
public class MyParentClass
{
    // CLASS MEMBERS (static): they live in the class and are shared by all instances.
    // In C# you access them ONLY through the class (MyParentClass.X), never through an object.

    // static readonly: assigned once, the COMPILER prevents reassigning it.
    // Constants use PascalCase in C#, never ALL_CAPS. For primitives and strings you could also use 'const'.
    public static readonly Info PublicConstantAttribute = new(
        "Constant class attribute",
        "I'm a constant class attribute. The compiler won't let anyone reassign me.");

    // FIELDS: always private, named _camelCase.
    // Anything visible outside the class (public or protected) is exposed through a property instead.
    private Info _protectedParentInstanceAttribute;
    private Info _privateParentInstanceAttribute;

    // Constructor: same name as the class and no return type. Equivalent to __init__.
    // 'this' is the equivalent of 'self', but it's implicit, you don't declare it as a parameter.
    public MyParentClass(Info publicParameter, Info protectedParameter, Info privateParameter)
    {
        PublicParentInstanceAttribute = publicParameter;

        // Validated on creation with the same rule the setters use.
        _protectedParentInstanceAttribute = EnsureContains(protectedParameter, "protected");
        _privateParentInstanceAttribute = EnsureContains(privateParameter, "private");
    }

    // Mutable shared state is exposed through a static property, never a public field.
    public static Info PublicNormalAttribute { get; set; } = new(
        "Normal class attribute",
        "I'm a normal class attribute, and I can be changed.");

    // INSTANCE PROPERTIES: they live in each object. Always PascalCase, whatever their visibility.

    // Auto-property: the compiler generates a hidden private backing field for you.
    public Info PublicParentInstanceAttribute { get; set; }

    // ENCAPSULATION with access modifiers + properties
    // Unlike Python, access modifiers are ENFORCED by the compiler:
    //   public    -> anyone
    //   protected -> this class and its child classes
    //   private   -> only this class (not even its children)
    //
    // A property is the C# equivalent of @property + .setter in one block.
    // This one is protected: only this class and its children can read or change it.
    protected Info ProtectedParentInstanceAttribute
    {
        get => _protectedParentInstanceAttribute;                                   // like @property
        set => _protectedParentInstanceAttribute = EnsureContains(value, "protected"); // like .setter ('value' is implicit)
    }

    // The data is private, but a public property gives controlled access to it.
    public Info PrivateParentInstanceAttribute
    {
        get => _privateParentInstanceAttribute;
        set => _privateParentInstanceAttribute = EnsureContains(value, "private");
    }

    // Tip: a read-only property is just { get; } and one only the class can change is { get; private set; }

    // METHODS: always PascalCase, whatever their visibility.

    // Static method. C# has no @classmethod: 'static' covers both @classmethod and @staticmethod.
    // It can use static members, but not instance members (there is no 'this').
    public static void MyStaticMethod()
    {
        Console.WriteLine(
            "I'm a static method, I don't receive the object, so I can only use static members " +
            $"like this: '{PublicConstantAttribute.Name}', '{PublicNormalAttribute.Name}'");
    }

    // Instance method: works with the object (this).
    // 'virtual' allows child classes to override it. In C# you have to opt in explicitly;
    // in Python every method can be overridden.
    public virtual void MyInstanceMethod()
    {
        Console.WriteLine(
            "I'm an instance method, I receive the object, and I can use the object's attributes " +
            $"like this: '{PublicParentInstanceAttribute.Name}' and the class attributes " +
            $"like this: '{PublicConstantAttribute.Name}'");
    }

    // POLYMORPHISM
    // The same method behaves differently depending on the object's class.
    public virtual void MyPolymorphicMethod()
    {
        Console.WriteLine("I'm the PARENT'S version of MyPolymorphicMethod(), and my child classes can override me.");
    }

    // Private static helper: only this class can use it, and it doesn't need an object.
    private static Info EnsureContains(Info value, string keyword)
    {
        ArgumentNullException.ThrowIfNull(value);

        // Always say how strings are compared (Ordinal = exact, case-sensitive).
        if (!value.Description.Contains(keyword, StringComparison.Ordinal))
        {
            throw new ArgumentException($"The value must contain the word '{keyword}'.", nameof(value));
        }

        return value;
    }
}