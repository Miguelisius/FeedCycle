alert("Código incrcustado en el head de una hoja externa");

document.addEventListener('DOMContentLoaded', function() {
    function addTable(){
        var myTableDiv = document.getElementById("myDynamicTable");
        var table = document.createElement('TABLE');
        table.border = '1';
        var tableBody = document.createElement('TBODY');

        table.appendChild(tableBody);
        var heading = ["Asignatura", "Acciones"];
        var tr = document.createElement('TR');
        tableBody.appendChild(tr);

        for (var i = 0; i < heading.length; i++) {
            var th = document.createElement('TH');
            th.appendChild(document.createTextNode(heading[i]));
            tr.appendChild(th);
        }
        
        myTableDiv.appendChild(table);
    }
    addTable();
});

