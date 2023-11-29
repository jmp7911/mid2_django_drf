

const $input = document.querySelector('input')
const $submit = document.querySelector('.submit')
const $wording = document.querySelector('.wording')
const $description = document.querySelector('.description')
const $history = document.querySelector('li')

async function getChatList(page=1) {
  const $search_history = document.getElementById('search_history')

  let response = await securedApiRequest('chat/model/?per-page=5&page='+page, 'GET');
  if (response.count > 0) {
    response.results.forEach(obj => {
      insertSearchHistory(obj)
    })
  }

}


getChatList();



$submit.addEventListener('click', async (e) => {
  console.log('click')
  e.preventDefault()
  document.body.className = "loading";

  /* chatbot  */
  response = await securedApiRequest('chat/api/', 'POST', {'input':$input.value});
  try {
    let jsonData = JSON.parse(response);

    $wording.innerHTML = `${jsonData.quote}`
    $description.innerHTML = `${jsonData.description}`

    const user = localStorage.getItem('user')
    const userData = JSON.parse(user)
    jsonData['user'] = userData['pk']
    let requestBody = {
      content: $input.value,
      user: userData['pk'],
      chat_reply: jsonData
    }

    console.log(requestBody)
    /* save chat */
    await securedApiRequest('chat/model/','POST', requestBody)

  } catch(e) {
    console.error(e)
    $wording.innerHTML = `${response}`
    $description.innerHTML = ``

} finally {
      document.body.className = "";
      $input.value = ''

  }
})

function insertSearchHistory(obj) {
  const $search_history = document.getElementById('search_history');

  const $history = document.createElement('li');
    $history.innerHTML = obj.content;
    $history.addEventListener('click', e=> {
      e.preventDefault();

      $wording.innerHTML = obj.chat_reply.quote;
      $description.innerHTML = obj.chat_reply.description === undefined ? '' : obj.chat_reply.description;
    })
  $search_history.appendChild($history)
}

async function removeHistory() {
  event.preventDefault();

  await securedApiRequest('chat/delete/','POST')


  window.location.reload()


}

