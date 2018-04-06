const rp = require('request-promise')
const Promise = require('bluebird')

function compute (expr) {
  if (expr.includes('+')) {
    const a = expr.split(' + ').map(s => parseInt(s.trim(), 10))
    return a[0] + a[1]
  } else if (expr.includes('*')) {
    const a = expr.split(' * ').map(s => parseInt(s.trim(), 10))
    return a[0] * a[1]
  } else if (expr.includes('-')) {
    const a = expr.split(' - ').map(s => parseInt(s.trim(), 10))
    return a[0] - a[1]
  } else if (expr.includes('/')) {
    const a = expr.split(' / ').map(s => parseInt(s.trim(), 10))
    return a[0] / a[1]
  } else if (expr.includes('%')) {
    const a = expr.split(' % ').map(s => parseInt(s.trim(), 10))
    return a[0] % a[1]
  } else {
    console.log('Unknown expression:', expr)
  }
}

async function main () {
  let data = await rp({
    uri: 'http://workshop.web1.sunshinectf.org/start?answer=no_answer',
    proxy: 'http://localhost:8888',
    json: true
  })
  const headers = {
    Authorization: data.token
  }
  while (data.questions) {
    const fHint = data.featureHintType
    console.log(data)
    const target = data.questions.filter(q => q[fHint] === data.featureHint)[0]
    let answer = compute(target.question)
    if (answer % 1 !== 0) answer = Math.floor(answer)
    data = await rp({
      uri: `http://workshop.web1.sunshinectf.org/submit`,
      qs: { answer },
      proxy: 'http://localhost:8888',
      headers,
      json: true
    })
    console.log('Got response:', data, 'for', target.question, 'with answer:', answer)
  }
}

main()
