export function whatsappHref(raw: string): string {
  let digits = raw.replace(/\D/g, '');
  if (digits.startsWith('00')) digits = digits.slice(2);
  if (digits.startsWith('0')) digits = `353${digits.slice(1)}`;
  return `https://wa.me/${digits}`;
}
