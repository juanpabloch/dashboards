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
