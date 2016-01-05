def foo(h):
    if h:
        print("h", h)
    else:
        print("nix ha")

h = None
foo(h)

print("nu kommt was")
h = "bar"

foo(h)