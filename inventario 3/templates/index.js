function mostrarEC(){
    let divEC = document.getElementById('e-commerce');
    let divMI = document.getElementById('mineria');
    let labelEC = document.getElementById('e-commerce');
    let labelMI = document.getElementById('mineria');

    labelEC.style.textDecoration='underline';
    labelMI.style.textDecoration='none';
                        
    divEC.style.display = 'block';
    divMI.style.display = 'none';
}

function mostrarMI(){
    let divEC = document.getElementById('e-commerce');
    let divMI = document.getElementById('mineria');
    let labelEC = document.getElementById('e-commerce');
    let labelMI = document.getElementById('mineria');

    labelMI.style.textDecoration='underline';
    labelEC.style.textDecoration='none';

    divMI.style.display = 'block';
    divEC.style.display = 'none';
}