export function parseValues(text) {
  if (typeof text !== 'string' || text.length > 200) throw new Error('Input is too long.');
  const tokens = text.split(',').map(t => t.trim());
  if (tokens.some(t => !/^[+-]?[0-9]{1,2}$/.test(t))) throw new Error('Use whole numbers from −99 to 99, separated by commas. No empty entries or expressions.');
  if (tokens.length < 2 || tokens.length > 10) throw new Error('Enter between 2 and 10 numbers.');
  return tokens.map(Number);
}
