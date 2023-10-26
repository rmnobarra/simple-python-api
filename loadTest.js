import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // número de usuários virtuais
  duration: '30s', // duração do teste
};

export default function () {
  let res = http.get('http://app:5000/users'); // substitua com o URL do seu endpoint
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
