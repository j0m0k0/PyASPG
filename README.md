# pyASPG

Todo:

    1. Add documents using pydoc

### Main Components of a Smart Power Grid

1. **[✅](https://emojipedia.org/check-mark-button) Power Generation** : Sources of electricity (e.g., power plants, solar panels, wind turbines).
2. **[✅](https://emojipedia.org/check-mark-button) Transmission** : High-voltage power lines that transport electricity from generation sources to substations.
3. **[✅](https://emojipedia.org/check-mark-button) Substation** : Receives electricity from transmitters, possibly transform it to a lower voltage, and then pass it to distributors.
4. **[✅](https://emojipedia.org/check-mark-button) Distribution** : Lower-voltage power lines that deliver electricity to consumers.
5. **[✅](https://emojipedia.org/check-mark-button) Prosumers** : End-users of electricity, such as households, businesses, and industries, that consume the electricity and able to produce as well.
6. **[✅](https://emojipedia.org/check-mark-button) Smart Meters** : Devices at consumer locations that measure electricity usage and communicate with utility companies and third-party data aggregators.
7. **[✅](https://emojipedia.org/check-mark-button) Communication Network** : Infrastructure that enables data exchange between smart meters, third-party data aggregators, and utility companies.
8. **Utility Companies** : Entities that manage the generation, transmission, and distribution of electricity.
9. **Third-Party Data Aggregators** : Companies that collect and manage data from consumers and communicate with utility companies.
10. **Control Systems** : Systems that manage the operation of the power grid, including demand response and load balancing.

### Steps to Build the Simulator

1. **Define the Data Structures** : Create classes for each component of the power grid.
2. **Establish Relationships** : Define how components interact with each other.
3. **Implement Basic Simulation Logic** : Simulate basic operations like power generation, transmission, distribution, and consumption.
4. **Integrate Third-Party Data Aggregators** : Add functionality for data collection and communication.
5. **Simulate Compromised Third-Party** : Introduce scenarios where third-party data aggregators are compromised and study the impact.

### Watt, Voltage and Current

Several important things have to happen in an electrical circuit for electricity to flow and for work to be done.

An electric circuit, uses electrons to carry the electricity.

**Voltage**: Electrical pressure, how strongly electricity is being pushed into the circuit

Voltage is important because many circuits are designed to only accept a certain number of volts.

**Ampere**: A unit of how much electrical charge is flowing past a given point in one second

**Power Formula**: P(watts) = I(amps) * V(volts)

Watts: How much energy is consumed

Watt (W) measures power, which is the rate of energy transfer. It tells you how much energy is used per second.

Voltage (V) measures electrical potential difference or pressure. It tells you how strong the electrical force is that pushes electric current through a circuit.

Current (measured in Amperes or Amps, A) is the flow of electric charge in a circuit. It tells you how many electrons are moving through a conductor per second.

### PyTest

- `assert` in python, will continue running the program if the assertion is true, otherwise will raise an exception.
- A test may fail because of the `assert` statement or even before that, if an exception happened.
- If we want to test whether we get an exception while running a specific code, we can test it using `with pytest.raises(ThatException)`. With this method we check to see if a certain exception happens or not.
- Class-based test, can have a setup method that runs before running of each test. you define it as `setup_method(self, method)`.
- We have another method called `teardown_method(self, method)`, which is the method for cleaning up after a test has finished.
- For running setup and teardown, you should run your tests using `pytest -s`.
- For having the concept of `setup_method` in functional test, we can use a concept called `pytest fixtures`.
- We define fixtures by `@pytest.fixture`.
- We can make our fixtures global across different test functions, by creating a file called `conftest.py` and then define the fixtures there.
- Pytest marking: Adding metadata to the tests, which can be used to organize, select, and control the execution of tests.
- For example, some tests may take a lot of time to run and be slow, some others be fast. You can later say that only run the fast tests or slow tests only. Usage: `@pytest.mark.slow` and for run we say: `pytest -m slow`
- Skip a test: `@pytest.mark.skip(reason='Feature is currently broken')`
- Expected failure: We know that a test is going to be failed: `@pytest.mark.xfail(reason='We know that is fails')`
- xfail is to say that ok we know that this test fails, but we want to keep track of them without having them counted as failed tests.
- Parameterizing: Clean way of trying the same test for various parameters. `@pytest.mark.parameterize("p1", "p2", [List of tuples])`
- Mocking: A technique used to isolate the system for testing. For example your function sends a request (it has cost, wait time and etc.), so you can mock it. Or another example is that you have a database and you don't want to mess it up.
- Other testing libraries like `unittest` can be used inside pytest without any issues.
- `import unittest.mock as mock` is used for mocking purposes.
- With using `@mark.patch("requests.get")` we can set the return value of a costly function and just mimic the behavior that we really called that function.
- Defining specific exceptions also can be useful. Like, customized exceptions for your situations so when you encounter them, you know what's going on.

### Sphinx

- Generates documentation from python docstrings.
- You first create a folder called 'docs'
- Then do `pip install sphinx` and it's theme called `sphinx-rtd-theme`
- Then you go the docs folder and run the command `sphinx-quickstart`
- Then get back and run this command: `sphinx-apidoc -o docs .`
-
