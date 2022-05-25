// USERS
// BANN USER
$('#banUserModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#banUserModalForm').attr('action', `${url}banned/${id}/`)
})

// ACTIVE USER
$('#activeUserModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#activeUserModalForm').attr('action', `${url}activate/${id}/`)
})

// EDIT USER
$('#editUserModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#editUserModalForm').attr('action', `${url}edit/${id}/`)
})

// DELETE USER
$('#deleteUserModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#deleteUserModalForm').attr('action', `${url}delete/${id}/`)
})


// DASHBOARDS
// Delete Dashboard
$('#deleteDashboardModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#deleteDashboardModalForm').attr('action', `${url}delete/${id}/`)
})

// DOMAINS
// Delete Domain
$('#deleteDomainModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#deleteDomainModalForm').attr('action', `${url}delete/${id}/`)
})


// Update Domain
$('#editDomainModal').on('show.bs.modal', (e)=>{
    const url = e.relatedTarget.baseURI;
    const button = $(e.relatedTarget);
    const id = button.data("id")
    $('#editDomainModalForm').attr('action', `${url}edit/${id}/`)
    const form = document.querySelector('#formFields')
    form.innerHTML = ''
    $.ajax({
        type: "GET",
        url: `get_domains/${id}`,
        success: function(data) {
            const div = document.createElement('div')
            div.innerHTML = `
            <div class="mb-3">
                <label for="id_name">Name:</label>
                <input class="form-control" value="${data.name}" type="text" name="name" maxlength="100" id="id_name">
            </div>
            <div class="mb-3">
                <label for="id_domain">Domain:</label>
                <input class="form-control" value="${data.domain}" type="text" name="domain" maxlength="255" id="id_domain">
            </div>
            `
            form.appendChild(div)
        }
    })
})




$(document).ready(function() {
    $('#dashboards').select2({
        placeholder: "Select a dashboard"
    });
    $('#dashboards_active').select2({
        placeholder: "Select a dashboard"
    });
});