import type { APIRoute } from 'astro';
import { liveAssets, csvFor, promptsTxt, fileNames } from '../../../../lib/assets';

export function getStaticPaths() {
  const out: { params: { file: string }; props: { body: string } }[] = [];
  for (const a of liveAssets) {
    if (a.kit) continue;
    const f = fileNames(a.slug);
    if (a.template) out.push({ params: { file: f.csv }, props: { body: csvFor(a) } });
    out.push({ params: { file: f.txt }, props: { body: promptsTxt(a) } });
  }
  return out;
}

export const GET: APIRoute = ({ params, props }) =>
  new Response(props.body as string, {
    headers: { 'Content-Type': params.file!.endsWith('.csv') ? 'text/csv; charset=utf-8' : 'text/plain; charset=utf-8' },
  });
