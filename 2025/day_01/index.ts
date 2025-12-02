import * as fs from 'fs';

const input = fs.readFileSync('day_01/input.txt', 'utf-8');

let zeroFound = 0;
let zerosClicked = 0;
let dial = 50;

input.split('\n').forEach((line) => {
  if (line.trim() === '') {
    return;
  }
  let num = parseInt(line.slice(1), 10);
  if (num > 100) {
    zerosClicked += Math.floor(num / 100);
    num = num % 100;
  }
  switch (line[0]) {
    case 'L':
      dial -= num;
      if (dial < 0 && dial + num !== 0) {
        zerosClicked++;
      }
      dial %= 100;
      if (dial < 0) {
        dial += 100;
      }
      break;
    case 'R':
      dial += num;
      if (dial > 100 && dial - num !== 0) {
        zerosClicked++;
      }
      dial %= 100;
      if (dial >= 100) {
        zerosClicked++;
        dial -= 100;
      }
      break;
    default:
      throw new Error(`Unknown direction: ${line[0]}`);
  }
  if (dial === 0) {
    zeroFound++;
    zerosClicked++;
  }
});

console.log(`Zero found ${zeroFound} times.`);
console.log(`Zeros clicked: ${zerosClicked}.`);
