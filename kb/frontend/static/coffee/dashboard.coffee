# dashboard.coffee

$(document).foundation(
  # accordion:
  #   multi_expand: true
  topbar:
    back_text: 'Zurück'
    )




formatDate = (timekb) ->
  date = new Date(timekb)
  [date.getDate(), date.getMonth()+1, date.getFullYear().toString().substr(2,2)].join('.')

createGraph = (id, data, labels) ->
  ykeys = _.map [1..labels.length], (num) -> 'value_' + num
  new Morris.Area(
    element: id
    data: data
    xkey: 'date'
    ykeys: ykeys
    labels: labels
    dateFormat: formatDate
    xLabelFormat: formatDate)


loadGraphData = (path, params) ->
  deferred = $.Deferred()
  $.get(path, params
  ).done((result) ->
    deferred.resolve result.data
  ).fail((xhr, status, error) ->
    deferred.reject 'Verbindung konnte nicht hergestellt werden'
  )
  return deferred.promise()

$.fn.loadGraphs = ->
  @each ->
    el = this
    graph = $('.graph', el)
    loadingIndicator = $('.graph-loading-indicator', el)

    path = graph.data('source')
    labels = graph.data('labels')
    id = graph.attr('id')

    [..., store] = window.location.pathname.split( '/' )
    params = {from: '2013-12-13', to:'2014-02-13'}
    params['store_id'] = store if store

    $.when(loadGraphData(path, params)
    ).always( ->
      loadingIndicator.hide()
      graph.show()
    ).done((data) ->
      window[id] = createGraph(id, data, labels)
    ).fail((error) ->
      graph.text error
    )

submitForm = (form) ->
  $self = $(form)
  return $.ajax
    type: $self.attr('method')
    url: $self.attr('action')
    data: JSON.stringify($self.serialize())

$.postJSON = (url, data) ->
  $.ajax
    type: 'POST'
    url: url
    data: JSON.stringify(data)

$ ->
  $('#shout-create-form').submit (ev) ->
    $.when(submitForm(this)
    ).always( ->

    ).done((data) ->
      console.log('success')
    ).fail((error) ->
      console.log(error)
    )

    ev.preventDefault()

  $('.graph-content').loadGraphs()
  csrftoken = $('meta[name=csrf-token]').attr('content')
  $.ajaxSetup
    beforeSend: (xhr, settings) ->
      xhr.setRequestHeader 'X-CSRFToken', csrftoken  unless /^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)
    contentType: 'application/json; charset=UTF-8'
    dataType: 'json'
