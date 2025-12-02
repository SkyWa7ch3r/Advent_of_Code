import { readFileSync } from 'fs';

const input = readFileSync('day_02/input.txt', 'utf-8').split(',');
const palindromicIds: number[] = [];
const atLeastTwiceIDs: number[] = [];

input.forEach((idRange) => {
  const [start, end] = idRange.split('-').map(Number);
  for (let id = start; id <= end; id++) {
    const idStr = id.toString();
    if (idStr.length === 1) continue;
    let mid = idStr.length / 2;
    if (idStr.length % 2 === 0) {
      const firstHalf = idStr.slice(0, mid);
      const secondHalf = idStr.slice(mid);
      if (firstHalf === secondHalf) {
        palindromicIds.push(id);
      }
    }
    for (let i = 0; i < mid; i++) {
      const digits = idStr.slice(0, i + 1);
      const repeated = digits.repeat(idStr.length / digits.length);
      if (repeated === idStr) {
        atLeastTwiceIDs.push(id);
        console.log(`Found atLeastTwiceID: ${id}`);
        break;
      }
    }
  }
});

console.log(
  `Sum of palindromic IDs: ${palindromicIds.reduce((a, b) => a + b, 0)}`
);

console.log(
  `Sum of atLeastTwiceIDs: ${atLeastTwiceIDs.reduce((a, b) => a + b, 0)}`
);
