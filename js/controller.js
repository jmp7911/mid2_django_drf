const url = `https://estsoft-openai-api.jejucodingcamp.workers.dev/`

const $input = document.querySelector('input')
const $button = document.querySelector('button')
const $wording = document.querySelector('.wording')

const data = []
data.push({
  "role": "system",
  "content": "assistant는 SBS 드라마 스토브리그의 대사를 작성한 작가입니다."
}, {
  "role": "user",
  "content": "에피소드 1의 명대사를 알려줘"
}, {
  "role": "assistant",
  "content": [{wording: "코치진들의 파벌싸움, 양쪽 파벌이 모두 무시하는 힘없는 감독, 어느새 소속이 부끄러워진 꼴찌의 이미지, 낙후된 시설 속에 떨어지는 의욕",
  description: "면접 중 드림즈의 문제점을 지적해달라는 질문에 대한 백승수의 답."}]
})


$button.addEventListener('click', e => {
  console.log('click')
  e.preventDefault()
  const contents = $input.value
  // data.push({
  //     "role": "user",
  //     "content": contents
  // })
  $input.value = ''

  chatGPTAPI()
})

function chatGPTAPI() {
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      redirect: 'follow'
  })
  .then(res => res.json())
  .then(res => {
      console.log(res)
      // 답변 온 것을 assistant로 저장
      $wording.innerHTML = `${res.choices[0].message.content}`
  })
}

export default $wording;
export {chatGPTAPI};