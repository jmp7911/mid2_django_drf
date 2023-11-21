const url = `https://estsoft-openai-api.jejucodingcamp.workers.dev/`

const $input = document.querySelector('input')
const $submit = document.querySelector('.submit')
const $wording = document.querySelector('.wording')
const $description = document.querySelector('.description')
const $history = document.querySelector('li')

const data = []


if (!localStorage.getItem('search_history')) {
  localStorage.setItem('search_history', JSON.stringify([]))
} else {
  const searchHistoryArr = JSON.parse(localStorage.getItem('search_history'));
  const $search_history = document.getElementById('search_history')
  searchHistoryArr.forEach(obj => {
    const $history = document.createElement('li');
    $history.innerHTML = obj.searchString;
    $history.addEventListener('click', e=> {
      e.preventDefault();
    
      $wording.innerHTML = obj.quote;
      $description.innerHTML = obj.description === undefined ? '' : obj.description;

    })
    $search_history.appendChild($history)
  })

}




data.push({
  "role": "system",
  "content": "assistant는 키워드만 보고 드라마 명장면 명대사를 찾아줍니다."
},
{
  "role": "user",
  "content": "스토브리그의 명대사를 알려줘"
}
)

const text = `1. 그 악의적인 편집은 계속 늘어나겠죠,
(드림즈는) 한 10년 이상 꼴찌할지도 모릅니다. 신생팀이 생긴다고 해도.
2. 백승수: 드림즈가 강해지길 바라십니까?
이세영: 당연하죠.
백승수: 모두가 그렇게 생각할까요?
3. 윤성복: 임동규도 그렇고, 단장님은 가장 단단히 박힌 돌만 건드리네요. 저같은 사람 자르는 게 쉬웠을 텐데요.
백승수: 박힌 돌에 이끼가 더 많을 겁니다.
4. 팀에 조금이라도 도움이 된다고 생각되는 일이면, 전 할 겁니다. 팀에 조금이라도 해가 된다고 생각되는 일이면 잘라 내겠습니다. 해 왔던 것들을 하면서, 안 했던 것들을 할 겁니다. 
회식 자리에서 구단 직원들에게 포부를 밝히며.
5. 백승수: 팀장님은 고세혁 팀장을 믿습니까?
이세영: 네, 믿어요. 오래 봐 온 분이에요.
백승수: 그게 다예요? 아무런 확인도 없이 그냥 그럴 사람이 아니다, 그게 믿는 겁니까? 그건 흐리멍텅하게 방관하는 겁니다.
이세영: 확인하는 순간 의심하는 거죠. 확실하지 않은 근거들보다 제가 봐 온 시간을 더 믿는 거예요.
백승수: 그 확실하지 않은 근거를 확실하게 확인해 볼 생각은 안 하셨어요?
이세영: 단장님은 의심 안 받아보셨어요? 그 때 기분 좋으셨어요?
백승수: 저는 아무 의심도 없는 흐리멍텅한 사람이랑 일하는 것보다는 차라리 나까지 의심하고 확인하길 바랍니다. 떳떳하면 기분 나쁠 것도 무서울 것도 없습니다.
3회 백승수, 이세영에게 고세혁을 믿냐며 의심하는 투로 질문하자 둘이 대립하며 대화할 때.
6. 이창권: 지금 소 잃고 외양간 고치라고요?
백승수: 네 고쳐야죠. "소 한 번 잃었는데 왜 안 고칩니까? 그거 안 고치는 놈은 다시는 소 못 키웁니다."
고세혁 前 팀장한테 돈을 주고 드래프트권을 얻으려고 했었던 이창권 선수를 설득할 때
7. 이세영: 애초에 우리가 이길 수 없는 게임이었어요...
백승수: 돈이 없어서 졌다. 과외를 못해서 대학을 못갔다. 몸이 아파서 졌다. 모두가 같은 환경일 수가 없고 각자 가지고 있는 무기를 가지고 싸우는 건데 핑계대기 시작하면 똑같은 상황에서 또 집니다.
8. 백승수: 계약을 하다 보니 화가 나던데요? 터무니없이 깎은 금액에 아랫놈들끼리만 그렇게 진흙탕 싸움을 한다는 게... 그 진흙탕 싸움에서 이기니까 더 화가 나고.
권경민: 됐고! 당신 연봉만큼 선수단 연봉 총액 올려줄 테니까 정정보도해! 너, 연봉 받고 일하라고!
백승수: 네? 그렇게 즉흥적으로 줄 수 있는 '그 돈' 때문에 우리가 협상 과정에서 얼마나 얼굴 붉히고 자존심 상했는지 잘 한 번 생각해 보십시오.
권경민: 어디까지 까불래?
백승수, 자신의 연봉 반납 및 재송그룹 재정 상태 의심 보도로 회장에게 까인 권경민이 쳐들어오자 화내며.
9.
"어떤 사람은 3루에서 태어나 놓고 자기들이 3루타를 친 줄 압니다. 뭐, 부끄러워할 필요는 없지만 자랑스러워하는 꼴은…. 보기 민망하죠."
자기처럼 말을 잘 들었으면 단장이 아니라 더 높은 자리에 앉았을 거라며 술 마시고 훈계하는 권경민에게 한 말
10. "우리들은 우리들이 할 일을 하면 됩니다."
11화에서 한재희가 배팅볼 투수부터 시작해서 사람 한 명, 한 명 늘린다고 해서 그게 팀의 성적에 반영되냐는 회의감 어린 반응에 대해 우리들은 우리들이 할 일을 해나가면 된다며 한 대사
11. 만약에, 간발의 차이로 우승을 하게 된다면, 이렇게라도 전지훈련을 와서 고생을 한 여러분들의 덕일 겁니다. 간발의 차이로 우승 놓치게 된다면 전지훈련을 이런 곳으로 오게 만든 제 탓일 겁니다. 여러분들이 할 일을 다한 전지훈련은 이렇게 끝이 났습니다. 고생하셨습니다. \
(맥주 캔을 따며)
자, 고생하셨습니다!
12화 전지훈련 겸 바이킹스와의 모의전 이후
12. "사장님 어딨어요?"
권경민: 백 단장 덕분에, 집으로 가셨지.
"뭐하는 겁니까, 지금?"
권경민: 커피 좀 타 와. 달지 않고 맛있게.
"뭐하는 거냐고!!"
12화에서 변치훈 홍보팀장이 느닷없이 재송그룹 감사팀의 조사를 받게 되자, 권경민에게 한 말
13.
성적은 단장 책임, 관중은 감독 책임. 그걸 믿는 편입니다. 단장은 스토브리그 기간과 새 시즌 동안에 팀이 더 강해지도록 세팅을 해야 되고, 감독이라면 경기장에 찾아온 관중들의 가슴 속에 불을 지펴야죠.
14화에서 백승수가 윤성복 감독에게 재계약한 이유를 설명하며
14. 
백승수: 저는 의리라는 두 글자가 때로는 선을 넘어서 더러운 걸 가리지만 그 자체를 나쁘게 보진 않습니다. 그런데, 지금은 어떻습니까? 지켜야 할 의리 같은 게 있습니까?
장우석: 권경민 사장.... 배신이라도 때리라는 겁니까?
백승수: 잘못된 용어를 쓰시네요. 배신을 때리는 게 아니라 불의를 봤으면 고발을 하라는 겁니다.
백승수, 장우석에게 이면계약서를 보여달라는 부탁을 하면서
15. 
권경민: (백승수에게만) 하, 이 새끼 봐라. 야, 내가 지금 어디 가는 줄 알아? 드림즈 해체 발표 기자회견. 재밌겠지? 같이 갈래?
백승수: 아니, 나도 많이 바쁠 것 같애.
15화에서, 드림즈의 최후를 알리는 권경민에게 한 말.
16. 
드림즈 단장 백승수입니다. 저에게 시간을 주신다면, 드림즈를 제가 매각하겠습니다.
15화 마지막 장면에서, 재송그룹 권일도 회장에게 드림즈를 해체가 아닌 매각하게 도와달라고 말하는 장면. \
날이 따뜻해진 걸 보면 단장의 시간은 지났습니다. 이제 감독과 선수들이 잘 하겠죠. 오늘의 결정만으로도 대표님께서는 대단한 결정을 하셨고, 제 발걸음은 한결 더 가벼워질 것 같습니다.
16화에서 단장직 해고를 받아들이겠다는 뜻을 전하며
17. 
백승수: 제가 이렇게 떠나는 건 저한테는 익숙한 일이고, 제가 떠나는 곳이 폐허가 되지 않은 건... 저한테는 처음 있는 일입니다.
이세영: 이번에도... 아무도 단장님을 지키지 못했네요.
백승수: 아니요, 저한테는, 처음으로 무언가를 지켜낸 것으로 기억될 것 같습니다. 이걸로도, 힘이 많이... 날 것 같습니다.[52]
16화에서, 단장직을 떠난 뒤 이세영과의 대화.
18. 
(권경민: 싸가지는 더럽게 없는데 일은 잘하는 사람이라고 소개를 했더니 좋아하던데요.)
백승수: 일만 잘하는 사람을 더 좋아할텐데 이분들한테는 좀 아쉽게 됐네요.
(권경민: 백 단장, 자신 있어요? 야구도 이제 겨우 익숙해졌는데 다른 종목을요.)
글쎄요, 해 봐야 알겠지만 뭐, 열심히 할 겁니다. (전화를 끊고 카메라를 바라보며) 다들 그렇지 않습니까?
16화 마지막 장면에서. 작중 치열하게 싸우다가 최후반부에 일을 소개시킬 정도로 개선된 것을 보면 나름 미운 정이 들었는지 악우 비슷한 관계가 된 것으로 추정된다.
19.
코치진들의 파벌싸움, 양쪽 파벌이 모두 무시하는 힘없는 감독, 어느새 소속이 부끄러워진 꼴찌의 이미지, 낙후된 시설 속에 떨어지는 의욕.
면접 중 드림즈의 문제점을 지적해달라는 질문에 대한 백승수의 답.
`;

const prompt = `
드라마 명대사: \`\`\`${text}\`\`\`

"숫자."로 장면이 구분되어 있습니다
`;

data.push({
  "role": "assistant",
  "content": prompt
}
)

$submit.addEventListener('click', async (e) => {
  console.log('click')
  e.preventDefault()
  
  const contents = `
  키워드와 관련된 장면이 있으면 장면 전체를 찾아줘.
  키워드는 이중 백틱(\`\`)으로 구분되어 있습니다.

  \`\`${$input.value}\`\`. 해당하는 결과가 없으면 '해당 장면을 찾을 수 없습니다'를 문자열로 응답 해줘. 결과가 있으면 씬 단위로 문장을 제외하고 장면번호,대사를 포함하고 scene,quote,description 키값을 사용하는 json객체 1개로 해줘`
  
  data.push({
      "role": "user",
      "content": contents
  })
  
  document.body.className = "loading";
  response = await chatGPTAPI()
  document.body.className = "";
  response.searchString = $input.value;
  insertSearchHistory(response);
  $input.value = ''
})

async function chatGPTAPI() {
  res = await (await fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      redirect: 'follow'
  })).json();
  
  console.log(res)
  // 답변 온 것을 assistant로 저장
  try {
    const jsonData = JSON.parse(res.choices[0].message.content);
    $wording.innerHTML = `${jsonData.quote}`
    $description.innerHTML = `${jsonData.description}`
    
    data.pop();

    return jsonData;
  } catch(e) {
    $wording.innerHTML = `${res.choices[0].message.content}`
    $description.innerHTML = ``
    data.pop();

    return {quote:res.choices[0].message.content};
  }

  

}

function insertSearchHistory(obj) {
  const $search_history = document.getElementById('search_history');
  const searchHistoryArr = JSON.parse(localStorage.getItem('search_history'));
  searchHistoryArr.push(obj);
  localStorage.setItem('search_history', JSON.stringify(searchHistoryArr));

  const $history = document.createElement('li');
  $history.innerHTML = obj.searchString;
  $history.addEventListener('click', e=> {
    e.preventDefault();
  
    $wording.innerHTML = obj.quote;
    $description.innerHTML = obj.description === undefined ? '' : obj.description;;

  })
  $search_history.appendChild($history)
}

function removeHistory() {
  event.preventDefault();
  localStorage.setItem('search_history', JSON.stringify([]))
  const $search_history = document.getElementById('search_history');

  $search_history.innerHTML = ''


}