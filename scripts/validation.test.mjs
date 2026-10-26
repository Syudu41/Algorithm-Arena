import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseValues} from '../web/validation.js';
test('valid signed arrays, duplicates and boundaries',()=>{
  assert.deepEqual(parseValues(' 5, -2, +0, 99, -99 '),[5,-2,0,99,-99]);
  assert.deepEqual(parseValues('7,7'),[7,7]);
});
test('invalid inputs never reach the renderer',()=>{
  for(const s of ['', '1','1,,2','1,2,','1.2,3','NaN,2','Infinity,2','1+1,2','100,2','-100,2','１,２','1e1,2','__import__(1),2',Array(11).fill('1').join(',')]) assert.throws(()=>parseValues(s),s);
});
