import { readFileSync } from 'fs';

const input = readFileSync('day_03/input.txt', 'utf-8').split('\n');

const joltages = input.map((batteryBank) => {
  let joltageDigits = {
    firstDigit: {
      value: -1,
      index: -1,
    },
    secondDigit: {
      value: -1,
      index: -1,
    },
  };
  for (let i = 0; i < batteryBank.length - 1; i++) {
    const joltageValue = parseInt(batteryBank[i]);
    if (joltageValue > joltageDigits.firstDigit.value) {
      joltageDigits.firstDigit = {
        value: joltageValue,
        index: i,
      };
      joltageDigits.secondDigit = { value: -1, index: -1 };
    } else if (
      joltageValue > joltageDigits.secondDigit.value &&
      joltageValue <= joltageDigits.firstDigit.value
    ) {
      joltageDigits.secondDigit = {
        value: joltageValue,
        index: i,
      };
    }
  }

  // Do the check for the last digit
  if (
    parseInt(batteryBank[batteryBank.length - 1]) >
    joltageDigits.secondDigit.value
  ) {
    joltageDigits.secondDigit = {
      value: parseInt(batteryBank[batteryBank.length - 1]),
      index: batteryBank.length - 1,
    };
  }

  return joltageDigits.firstDigit.value * 10 + joltageDigits.secondDigit.value;
});

console.log(`Sum of joltages: ${joltages.reduce((a, b) => a + b, 0)}`);

// We now need 12 digits from each battery bank

const bigJoltages = input.map((batteryBank) => {
  let joltageDigits: number[] = [];
  for (let i = 0; i < batteryBank.length; i++) {
    const battery = parseInt(batteryBank[i]);
    // While the current battery is larger than the last digit in the array
    // and we have enough digits left to fill to 12, pop the last digit
    // While also ensuring we don't empty the stack
    while (
      joltageDigits.length > 0 &&
      battery > joltageDigits[joltageDigits.length - 1] &&
      joltageDigits.length - 1 + (batteryBank.length - i) >= 12
    ) {
      joltageDigits.pop();
    }
    // If we have less than 12 digits, add the current battery
    if (joltageDigits.length < 12) {
      joltageDigits.push(battery);
    }
  }

  return parseInt(joltageDigits.join(''));
});
console.log('Big joltages:', bigJoltages);

console.log(`Sum of big joltages: ${bigJoltages.reduce((a, b) => a + b, 0)}`);
