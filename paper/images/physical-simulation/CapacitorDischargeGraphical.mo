model capacitor
  Modelica.Electrical.Analog.Basic.Capacitor capacitor(C = 1, v(start = 5))  annotation(
    Placement(visible = true, transformation(origin = {-26, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Electrical.Analog.Basic.Resistor resistor(R = 1)  annotation(
    Placement(visible = true, transformation(origin = {-16, -16}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(visible = true, transformation(origin = {-36, -36}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(resistor.n, ground.p) annotation(
    Line(points = {{-16, -26}, {-36, -26}}, color = {0, 0, 255}));
  connect(capacitor.n, ground.p) annotation(
    Line(points = {{-36, 10}, {-36, -26}}, color = {0, 0, 255}));
  connect(capacitor.p, resistor.p) annotation(
    Line(points = {{-16, 10}, {-16, -6}}, color = {0, 0, 255}));

annotation(
    uses(Modelica(version = "4.0.0")));
end capacitor;
