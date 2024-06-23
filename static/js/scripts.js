document.addEventListener('DOMContentLoaded', function() {
    const dataUrl = 'http://127.0.0.1:7000/userInfo/';  // JSON 데이터를 가져올 API URL
    const loadButton = document.getElementById('load-button');
    const table = document.getElementById('data-table');

    loadButton.addEventListener('click', function() {
        fetch(dataUrl)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.querySelector('#data-table tbody');
                tableBody.innerHTML = ''; // 테이블을 초기화합니다.

                data.forEach(item => {

                    const row = document.createElement('tr');

                    const numCell = document.createElement('td');
                    numCell.textContent = item.회원번호;
                    row.appendChild(numCell);
                    
                    const nameCell = document.createElement('td');
                    nameCell.textContent = item.회원이름;
                    row.appendChild(nameCell);
                    
                    const gradeCell = document.createElement('td');
                    gradeCell.textContent = item.등급;
                    row.appendChild(gradeCell);

                    const scoreCell = document.createElement('td');
                    scoreCell.textContent = item.이용점수;
                    row.appendChild(scoreCell);

                    const addressCell = document.createElement('td');
                    addressCell.textContent = item.회원주소;
                    row.appendChild(addressCell);

                    const discountCell = document.createElement('td');
                    discountCell.textContent = item.등급별할인율;
                    row.appendChild(discountCell);

                    tableBody.appendChild(row);
                });

                table.style.display = 'table'; // 테이블을 표시합니다.
            })
            .catch(error => {
               
                console.error('Error fetching the data:', error);
            });
    });
});
