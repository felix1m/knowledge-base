# dashboard.coffee

$ ->
  $("#create-shout-btton").click ->
    createShout()

  mutlipleSelects = $("select[multiple]")

  if Modernizr.touch
    checkboxes = $("input:checkbox").each (index) ->
      parent = $(this).parent()
      $('label', parent).clone().prependTo(parent.parent());
      parent.addClass('switch round')
  else
    mutlipleSelects.each (index) ->
      $this = $(this)
      $this.zmultiselect
          live: false
          selectAll: false


  $("#store-detail-tabs").on "toggled", (event, tab) ->
    if tab[0].id is 'store-panel-4'
      graph_ids = ['total_kbs', 'daily_kbs', 'user_count', 'shout_views', 'reward_count', 'daily_rewards']

      for graph_id in graph_ids
        graph = window[graph_id]
        # redraw_fun = (graph)->
        #   console.log graph
        #   return graph.redraw()
        # setTimeout(redraw_fun(graph, graph_id), 0) if graph
        graph.redraw() if graph

createShout = ->
  deferred = $.Deferred()

  path = '/shouts/create'
  params = {name: 'This is a testshout.#ÄÖÜ?á', start: '2014-06-10', end: '2015-06-10', affiliated_users: 1, age_max: 30, age_min: 16, activity: true, returning_users: true, budget_cap: 20.0, stores:[2]}
  console.log(params)

  $.postJSON(path, params
  ).done((result) ->
    console.log('Success:')
    console.log(result)
  ).fail((xhr, status, error) ->
    console.log(error)
    console.log(xhr)
    console.log(xhr)
  )
  return deferred.promise()
