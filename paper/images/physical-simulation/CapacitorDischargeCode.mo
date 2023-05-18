model CapacitorDischarge
  parameter Real C = 1;
  parameter Real Resistance = 1;
  parameter Real initialVoltage = 5;
  Real voltage(start=initialVoltage);
equation
  der(voltage) = -voltage / (C * Resistance);
end CapacitorDischarge;
