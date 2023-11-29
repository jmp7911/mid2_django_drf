const params = new URL(location).searchParams;

async function getBoardList(page=1) {
  const $search_history = document.getElementById('search_history')

  let response = await securedApiRequest('quote/?per-page=5&page='+page, 'GET');
  document.getElementById('count').innerText = response.count
  if (response.count > 0) {
    response.results.forEach(obj => {
      viewBoardList(obj)
    })
  }

  const $pagination = document.getElementsByClassName('pagination')
  const $previous = document.createElement('a')
  $previous.href = 'quote.html?page='+ (Number(page)-Number(1))
  const $previousImg = document.createElement('img')
  $previousImg.src = './img/prev.png'
  $previous.appendChild($previousImg)
  const $next = document.createElement('a')
  $next.href = 'quote.html?page='+ (Number(page)+Number(1))
  const $nextImg = document.createElement('img')
  $nextImg.src = './img/next.png'
  $next.appendChild($nextImg)

  if (response.previous != null) {
    $pagination[0].appendChild($previous)
  }
  if (response.next != null) {
    $pagination[0].appendChild($next)
  }
}
const page = params.get('page') != null ? params.get('page') : 1
getBoardList(page)

function viewBoardList(obj) {
  const $main = document.getElementById('main');

  const $document = document.createElement('tr')
  const $number = document.createElement('td')
  $number.innerText = obj.id
  const $title = document.createElement('td')
  const $title_a = document.createElement('a')
  $title_a.innerText = obj.title
  $title_a.href='view.html?id='+obj.id
  $title.appendChild($title_a)
  const $user = document.createElement('td')
  $user.innerText = obj.user.email
  const $created_at = document.createElement('td')
  const created_at = new Date(obj.created_at)
  $created_at.innerText = created_at.getFullYear()+'.'+(created_at.getMonth()+Number(1))+'.'+created_at.getDate()
  const $is_apply = document.createElement('td')
  $is_apply.innerText = obj.is_apply

  $document.appendChild($number)
  $document.appendChild($title)
  $document.appendChild($user)
  $document.appendChild($created_at)
  $document.appendChild($is_apply)
  $main.appendChild($document)



}